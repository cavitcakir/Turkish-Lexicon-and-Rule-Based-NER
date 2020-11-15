import re
#file
lexicon_persons_file = open("lexicon_person.txt", "r")
lexicon_locations_file = open("lexicon_location.txt", "r")
lexicon_organizations_file = open("lexicon_organization.txt", "r")

lexicon_persons = [i.strip().split("\n")[0]for i in lexicon_persons_file.readlines()]
lexicon_locations = [i.strip().split("\n")[0]for i in lexicon_locations_file.readlines()]
lexicon_organizations = [i.strip().split("\n")[0]for i in lexicon_organizations_file.readlines()]

pre_keywords_person_file = open("Keywords/pre_keywords_person.txt", "r")
after_keywords_person_file = open("Keywords/after_keywords_person.txt", "r")

pre_keywords_organization_file = open("Keywords/pre_keywords_organization.txt", "r")
after_keywords_organization_included_file = open("Keywords/after_keywords_organization_included.txt", "r")
after_keywords_organization_excluded_file = open("Keywords/after_keywords_organization_excluded.txt", "r")

pre_keywords_location_file = open("Keywords/pre_keywords_location.txt", "r")
after_keywords_location_included_file = open("Keywords/after_keywords_location_included.txt", "r")
after_keywords_location_excluded_file = open("Keywords/after_keywords_location_excluded.txt", "r")

pre_keywords_date_file = open("Keywords/pre_keywords_date.txt", "r")
between_keywords_date_file = open("Keywords/between_keywords_date.txt", "r")
after_keywords_date_file = open("Keywords/after_keywords_date.txt", "r")

pre_keywords_time_file = open("Keywords/pre_keywords_time.txt", "r")
after_keywords_time_file = open("Keywords/after_keywords_time.txt", "r")

pre_keywords_persons = [i.strip().split("\n")[0]for i in pre_keywords_person_file.readlines()]
after_keywords_persons = [i.strip().split("\n")[0]for i in after_keywords_person_file.readlines()]

pre_keywords_organizations = [i.strip().split("\n")[0]for i in pre_keywords_organization_file.readlines()]
after_keywords_organizations_included = [i.strip().split("\n")[0]for i in after_keywords_organization_included_file.readlines()]
after_keywords_organizations_excluded = [i.strip().split("\n")[0]for i in after_keywords_organization_excluded_file.readlines()]


pre_keywords_location = [i.strip().split("\n")[0]for i in pre_keywords_location_file.readlines()]
after_keywords_location_included = [i.strip().split("\n")[0]for i in after_keywords_location_included_file.readlines()]
after_keywords_location_excluded = [i.strip().split("\n")[0]for i in after_keywords_location_excluded_file.readlines()]

pre_keywords_date = [i.strip().split("\n")[0]for i in pre_keywords_date_file.readlines()]
between_keywords_date = [i.strip().split("\n")[0]for i in between_keywords_date_file.readlines()]
after_keywords_date = [i.strip().split("\n")[0]for i in after_keywords_date_file.readlines()]

pre_keywords_time = [i.strip().split("\n")[0]for i in pre_keywords_time_file.readlines()]
after_keywords_time = [i.strip().split("\n")[0]for i in after_keywords_time_file.readlines()]

import sys
data_path = sys.argv[1]
testdata = open(data_path)
line_number = 0

def tokenize(sf):
    sf = sf.split()
    new_sf = []
    for i in range(len(sf)):
        if("-" in sf[i]):
            news = sf[i].split("-")
            for j in range(len(news)):
                new_sf.append(news[j].split(",")[0])
                if j != len(news)-1:
                    new_sf.append("-")
        else:
            new_sf.append(sf[i].split(",")[0])

        if sf[i][-1] == ",":
            new_sf.append(",")
    return new_sf

def ensamble_matches(tagged):
    while_flag = True
    found_one = False
    while while_flag:
        for i in range(len(tagged)):
            for j in range(len(tagged)):
                if i != j:
                    iStart = tagged[i][0][0]
                    iEnd = tagged[i][0][1]
                    jStart = tagged[j][0][0]
                    jEnd = tagged[j][0][1]
                    iType =tagged[i][1]
                    jType =tagged[j][1]
                    # print(iStart, iEnd, jStart, jEnd)

                    if (iType==jType) and (iEnd+1 == jStart) and line[iEnd] == " ": # bastan ekliceksem
                        new_triple = ((iStart,jEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break

                    if (iType==jType) and  (iStart == jEnd+1) and line[iStart] == " ": # sondan
                        new_triple = ((jStart,iEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break

                    if (iType==jType) and (iType == "ORGANIZATION\t") and (iEnd+4 == jStart): # ve
                        new_triple = ((iStart,jEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break

                    if (iType==jType) and (iType == "ORGANIZATION\t") and  (iStart == jEnd+4): # ve
                        new_triple = ((jStart,iEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break

                    if (iType==jType) and (iEnd == jStart): # bastan ekliceksem
                        new_triple = ((iStart,jEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break
                    if (iType==jType) and  (iStart == jEnd): # sondan
                        new_triple = ((jStart,iEnd),iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break

                    if (iType==jType) and (iStart <= jStart) and (iEnd >= jEnd):  # daha genis yakaladiysam
                        new_triple = ((iStart,iEnd), iType)
                        tagged[i] = new_triple
                        del tagged[j]
                        found_one = True
                        break
                    # elif (Type== "ORGANIZATION\t") and (iStart == jStart) and (iEnd == jEnd):  # daha genis yakaladiysam
                    #     new_triple = ((iStart,iEnd), iType)
                    #     tagged[i] = new_triple
                    #     del tagged[j]
                    #     found_one = True
                    #     break

                    if (iType==jType) and (iStart >= jStart) and (iEnd <= jEnd): # daha dar yakaladiysam
                        del tagged[i]
                        found_one = True
                        break
            if found_one == True:
                break
        if found_one == True:
            found_one = False
        else:
            while_flag = False
    return tagged

def remove_keywords(tagged,line):
    all_keywords = pre_keywords_organizations +  after_keywords_organizations_excluded + pre_keywords_location + after_keywords_location_excluded + after_keywords_date +pre_keywords_persons + after_keywords_persons
    for i in range(len(tagged)):
        if(len(tagged) > 0 and i < len(tagged)-1):
            tag = tagged[i]
            tagStart = tag[0][0]
            tagEnd = tag[0][1]
            word = line[tagStart:tagEnd]
            word_list = word.split()
            keyword_flag = True
            while keyword_flag:
                found = False
                for each in all_keywords:
                    if len(word_list)>0 and word_list[0] == each:
                        found = True
                        break
                if found:
                    popped = word_list.pop(0)
                    tagStart += len(popped)+1
                else:
                    break

            keyword_flag = True
            while keyword_flag:
                found = False
                for each in all_keywords:
                    if len(word_list)>0 and word_list[-1] == each:
                        found = True
                        break
                if found:
                    popped = word_list.pop(-1)
                    tagEnd -= len(popped)+1
                else:
                    break

            if(tagStart<tagEnd):
                new_span = (tagStart,tagEnd)
                tagged[i] = (new_span,tag[1])
            else:
                tagged.pop(i)
                i-=1


    return tagged

def handle_match(catched_keyword, keywords, info, match, tagged , line_number, flag, line ):
    catched = match[0]
    newStart = match.span(0)[0]
    newEnd = match.span(0)[1]
    if newStart < newEnd:
        while line[newStart] == " ":
            newStart += 1
        # print("elmca1",line[newEnd-1])
        while line[newEnd-1] == " ":
            newEnd -= 1
        new_span = (newStart,newEnd)
        # print(line[newStart:newEnd], catched, len(catched))
        for each in keywords: # ex. (prof. dr.) catched before but now we catch (prof).
            if catched in each: ###########################eger parametreye 2 listeyi de verirsen, hem bastan hem sondan yakaladiginda patliyiiir
                flag = True
                break
            if info == "PERSON\t":
                for catch in catched.split():
                    if catch == each:
                        flag = True
                        break
                if flag == True:
                    break

        for i in range(len(tagged)):
            if flag == True:
                break
            if(new_span == tagged[i][0]):
                flag = True
                break
            tagStart = tagged[i][0][0]
            tagEnd = tagged[i][0][1]

            # print(newStart,newEnd,tagStart,tagEnd)

            # if (newStart <= tagStart) and (newEnd >= tagEnd) and info[:-1] == tagged[i][1]:  # daha genis yakaladiysam
            if (newStart <= tagStart) and (newEnd >= tagEnd):  # daha genis yakaladiysam tagten bagimsiz
                new_triple = (new_span, info[:-1])
                # print(match.re)
                tagged[i] = new_triple
                flag = True
                break
            elif (tagStart < newStart) and (newEnd >= tagEnd) and info[:-1] == "ORGANIZATION\t" and catched.isupper():
                flag = True
                break

            # if (newStart >= tagStart) and (newEnd <= tagEnd) and info[:-1] == tagged[i][1]: # daha dar yakaladiysam
            if (newStart >= tagStart) and (newEnd <= tagEnd): # daha dar yakaladiysam
                flag = True
                # print(line[newStart:newEnd],"yakalamistim ama bu var diye saldim", line[tagStart:tagEnd])
                break

            if(newEnd == tagStart and info[:-1] == tagged[i][1] ): # bastan ekliceksem
                new_triple = ((newStart,tagEnd),info[:-1])
                tagged[i] = new_triple
                flag = True
                break

            if(newStart == tagEnd and info[:-1] == tagged[i][1] ): # sondan
                new_triple = ((tagStart,newEnd),info[:-1])
                tagged[i] = new_triple
                flag = True
                break

    if flag == True:
        flag = False
    else:
        if(new_span[0] < new_span[1]):
            tagged.append((new_span, info[:-1]))
    return tagged


# org -> loc -> time -> kisi

for line in testdata:
    line_number += 1
    tagged = []
    flag = False
    ex_line =""
    line = re.sub(r'"', '', line)
    for each in line.split():
        ex_line += " " + each
    line = ex_line[1:]
    # print(line)
# #organization
    for pre_organization in pre_keywords_organizations:
        search_regex =  r"(?<=" + pre_organization + r" )(\s*([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*|ve)){1,6}"
        # print(search_regex)
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(pre_organization, pre_keywords_organizations, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)
    for after_organization in after_keywords_organizations_excluded:
        search_regex= r"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*|ve)\s*){1,6}(?=([']\w*\s*)? " + after_organization + r"\w*)"
        # print(search_regex)
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(after_organization, after_keywords_organizations_excluded, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)
    for after_organization in after_keywords_organizations_included:
        search_regex= r"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]+|ve)\s*){1,6}( "+after_organization+r"\w*)"
        # print(search_regex)
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(after_organization, after_keywords_organizations_included, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)


# #location
    for preLocation in pre_keywords_location:
        search_regex =  r"(?<=" + preLocation + r" )(\s*([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)){1,6}"
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(preLocation, pre_keywords_location, "LOCATION\t" ,match, tagged, line_number, flag, line)

    for after_location in after_keywords_location_excluded:
        search_regex = r"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)\s*){1,6}(?=([']\w*\s*)? " + after_location + r"\w*)"
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(after_location, after_keywords_location_excluded, "LOCATION\t" ,match, tagged, line_number, flag, line)

    for after_location in after_keywords_location_included:
        search_regex = r"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)\s*){1,6}( " + after_location + r"\w*)"
        # print(search_regex)
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(after_location, after_keywords_location_included, "LOCATION\t" ,match, tagged, line_number, flag, line)

# #date
    for month in between_keywords_date:
        # search_regex = r"(\d{1,4} )?(" + month + r"(')?\w*)( \d{1,4}\w*([']\w*)?)?"
        search_regex = r"(\d{1,4} )?("+month+r")( \d{1,4})?" # NNNN? Ay NNNN?
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(month, between_keywords_date, "TIME\t" ,match, tagged, line_number, flag, line)

        search_regex = r"(( )?((-|(\d{1,4}))( )?)*)?("+month+r")" # NNNN? Ay NNNN?
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(month, between_keywords_date, "TIME\t" ,match, tagged, line_number, flag, line)


    for preDate in pre_keywords_date: #ayin, m.o
        search_regex =  r"(" + preDate + r"([']\w*)? )(\d{1,4})([']\w*)?"
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(preDate, pre_keywords_date, "TIME\t" ,match, tagged, line_number, flag, line)

    for afterDate in after_keywords_date: #tarihinde
        search_regex = r"(\d{1,4} )(?=([']\w*)? "+afterDate+r"\w*)" # BURASI COKOMELLI
        # print(search_regex)

        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(afterDate, after_keywords_date, "TIME\t" ,match, tagged, line_number, flag, line)

        # search_regex = r"(\d{1,4})?(?=([']\w*)? "+afterDate+r"\w*)" # BURASI COKOMELLI
        # matched = re.finditer(search_regex, line)
        # for match in matched:
        #     tagged = handle_match(afterDate, after_keywords_date, "TIME\t" ,match, tagged, line_number, flag, line)

    for preTime in pre_keywords_time:
        search_regex =  r"(" + preTime + r" )(([0-2][0-3])|[0-9])([:.]([0-5][0-9]))?"
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(preTime, pre_keywords_time, "TIME\t" ,match, tagged, line_number, flag, line)

    date_regex_list = []
    date_regex_list.append(r"\d{2}[./-]\d{2}[./-]\d{2,4}") # 22.22.2222
    date_regex_list.append(r"(([A-Z]+)|\d+)(. yüzyıl)") # V. yüzyıl
    date_regex_list.append(r"(([0-2][0-3])|[0-9])[:.]([0-5][0-9])") # 23:59
    date_regex_list.append(r"([12][0-9]{3})(?=[']\w*)?") # 1997

    for date_regex in date_regex_list:
        matched = re.finditer(date_regex, line)
        for match in matched:
            tagged = handle_match("", [], "TIME\t" ,match, tagged, line_number, flag, line)

#person
    for prePerson in pre_keywords_persons:
        search_regex =  r"(?<=" + prePerson + r" )(\s*[A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*){1,6}"
        # print(search_regex)
        # III.I. II. IV. V. VI.
        matched = re.finditer(search_regex, line)
        for match in matched:
            # print(match[0], len(match[0]))
            tagged = handle_match(prePerson, pre_keywords_persons, "PERSON\t" ,match, tagged, line_number, flag, line)
            # print(tagged)
    search_regex =  r"(" + r"(III\.|I\.|II\.|IV\.|V\.|VI\.)" + r" )(\s*[A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*){1,6}"
    # print(search_regex)
    # (III\.|I\.|II\.|IV\.|V\.|VI\.)
    matched = re.finditer(search_regex, line)
    for match in matched:
        # print(match[0], len(match[0]))
        tagged = handle_match(prePerson, pre_keywords_persons, "PERSON\t" ,match, tagged, line_number, flag, line)

    for afterPerson in after_keywords_persons:
        search_regex = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*){1,6}(?=([']\w*)? " + afterPerson + r"\w*)"
        matched = re.finditer(search_regex, line)
        for match in matched:
            tagged = handle_match(afterPerson, after_keywords_persons + pre_keywords_persons, "PERSON\t" ,match, tagged, line_number, flag, line)


    # lexicon_persons = ["Kaya","Kapagan","Elma Elmaci", "Kaya Kapagan","A.","B.", "A. B."]
    # lexicon_locations = ["İzmir","İstanbul","ABD"]
    # lexicon_organizations = ["TUBİTAK", "Tekke", "Zaviyeler", "Tekke ve Zaviyeler"]

    # for tag in tagged:
    #     print("Before lexicon:", line_number, "\t", tag[1], "\t" , line[tag[0][0]:tag[0][1]], "\t" , tag[0][0],"," ,tag[0][1])


    tagged = remove_keywords(tagged,line)

    capitalized_word = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)" #  every CapWord
    consecutive_cap_word = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)+" # consecutive but maybe " " at the end
    consecutive_cap_word_with_special = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*((')|\s*))+" # consecutive but maybe " " at the end
    consecutive_cap_word_with_special2 = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*[']?)+"
    cap_and_dot = r"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\.( )?)"
    consecutive_cap_word_with_ve = r"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)|(ve\s*))+" # consecutive with ve but maybe " " at the end

    org_regex = []
    org_regex.append(consecutive_cap_word)
    org_regex.append(consecutive_cap_word_with_ve)
    org_regex.append(capitalized_word)
    org_regex.append(cap_and_dot)
    for search_regex in org_regex:
        matched = re.finditer(search_regex, line)
        for match in matched:
            aranacak_tag = match[0]
            i = -1
            while match[0][i] == " ":
                aranacak_tag = match[0][:i]
                i-=1
            for each in lexicon_organizations:
                # print(each)
                if aranacak_tag == each:
                    # print(aranacak_tag)
                    # print(match.re)
                    tagged = handle_match("", after_keywords_organizations_excluded + after_keywords_organizations_included + pre_keywords_organizations, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)

            # if aranacak_tag in lexicon_organizations:
            #     tagged = handle_match("", after_keywords_organizations_excluded + after_keywords_organizations_included + pre_keywords_organizations, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)

    loc_regex = []
    loc_regex.append(consecutive_cap_word)
    loc_regex.append(consecutive_cap_word_with_ve)
    loc_regex.append(capitalized_word)
    loc_regex.append(cap_and_dot)
    for search_regex in loc_regex:
        matched = re.finditer(search_regex, line)
        for match in matched:
            aranacak_tag = match[0]
            i = -1
            while match[0][i] == " ":
                aranacak_tag = match[0][:i]
                i-=1
            if aranacak_tag in lexicon_locations:
                tagged = handle_match("", after_keywords_location_excluded + after_keywords_location_included + pre_keywords_location, "LOCATION\t" ,match, tagged, line_number, flag, line)

    person_regex = []
    person_regex.append(consecutive_cap_word)
    person_regex.append(capitalized_word)
    person_regex.append(cap_and_dot)
    person_regex.append(consecutive_cap_word_with_special)
    person_regex.append(consecutive_cap_word_with_special2)
    for search_regex in person_regex:
        matched = re.finditer(search_regex, line)
        for match in matched:
            aranacak_tag = match[0]
            i = -1
            while match[0][i] == " ":
                aranacak_tag = match[0][:i]
                i-=1
            if aranacak_tag in lexicon_persons:
                tagged = handle_match("", after_keywords_persons + pre_keywords_persons, "PERSON\t" ,match, tagged, line_number, flag, line)


    all_capitalized_word = r" ([A-ZÇĞİÖŞÜ]){3}(?= |'|/')"
    matched = re.finditer(all_capitalized_word, line)
    for match in matched:
        tagged = handle_match("", after_keywords_organizations_excluded + after_keywords_organizations_included + pre_keywords_organizations, "ORGANIZATION\t" ,match, tagged, line_number, flag, line)


#bastirt
    # print("Line:", line_number,"bitti")
    tagged = ensamble_matches(tagged)
    tagged_deneme = sorted(tagged, key=lambda tup: tup[0][0])
    for tag in tagged_deneme:
        print("Line:", line_number, tag[1], line[tag[0][0]:tag[0][1]])






#hocanin verdikleri
    # for line in testdata:
    #     line_number += 1
    #     # RULE_EXAMPLE 1
    #     if 'Üniversite' in line:
    #         print("Line:" ,line_number , "ORGANIZATION", re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]* Üniversite\w+', line))
    #     # RULE_EXAMPLE 2
    #     if 'yıl' in line:
    #         print("Line:" ,line_number , "DATE", re.findall(r'\d{4}(?=\s+yıl\w+)', line))
    #     # RULE_EXAMPLE 3
    #     if 'Prof. Dr.' in line:
    #         print("Line:" ,line_number , "PERSON", re.findall(r'(?<=Prof. Dr. )[A-ZÇĞİÖŞÜ][a-zçğıöşü]*\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]*', line))
    # RULE_EXAMPLE 4
    # for uppercaseWord in re.finditer(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*', line):
    #     uppercaseWord = line[uppercaseWord.start():uppercaseWord.end()]
    #     print("######################################",uppercaseWord)
    #     if uppercaseWord in LOCATIONS:
    #         print("Line:" ,line_number , "LOCATION", uppercaseWord)
