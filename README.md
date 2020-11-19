# Lexicon and Rule-based Named Entity Recognition


#### Structure of file:
- Environment Information and How to Run
- Brief Introduction
- File Structure & Script Information & Keyword Information
- Regex Descriptions
- Sources

#### Dataset
- Mail me if you want to access to data and whole lexicon set which used in project

#### Environment Information:
    OS: macOS Catalina 10.15.7
    Python Version: 3.8.3
    To run: python ner.py input_file_path > output_file_path


#### Brief Introduction:
    I collected Turkish and English text data which are labeled for NER. With the help of the 17 script cleaned them and created lexicons.
    I created keywords files in order to catch NER tags with only regex.


#### File Structure:
    -   "ner.py" is the main NER script.

    -   Lexicons are listed as follows:
            "lexicon_organization.txt"
            "lexicon_location.txt"
            "lexicon_person.txt"

    -   Scripts that I used to create lexicons are listed under "Scripts" folder. I used 17 scripts to gather and process the lexicon files.

            -   Each subfolders name are structed like: "DATASET-NAME_Related"
                    Scipt files under subfolders are named as "DATASET-NAME.py"
                        Extracted data files names as follows:
                            "DATASET-NAME_organizations.txt"
                            "DATASET-NAME_locations.txt"
                            "DATASET-NAME_persons.txt"
                    Also under same folder you can find the raw data that I used to create those context based seperated txt files.

            -   After extracted data from raw datasets, I did 6 steps in order to get final lexicons, I did some copy paste operations and used 3 scripts in "data_prep" folder which is subfolder of "Scripts".
                    -   Step 1: I created 3 different files and put all the data that I gathered from different sources into 3 seperate files correspond to their contents(organizations, locations, persons).
                            These files are named as "lexicon_CONTENT_with_duplicate.txt"
                    -   Step 2: I extracted all duplicates with the script which named as "check_duplicate.py".
                            These files are named as "lexicon_CONTENT_no_duplicate.txt"
                    -   Step 3: I extracted all the intersections between files into "all_intersections.txt" with the script named as "remove_spesific.py".
                            These files are named as "lexicon_CONTENT_no_intersection_duplicate.txt"
                    -   Step 4: I used "handle_insersections.py" script in order to find suitable CONTENT for each word in "all_intersections.txt" which is created at Step 3.
                            I extracted that suitable words as "CONTENT_eklenecekler.txt"
                    -   Step 5: I created 3 different files and put all the data I gathered from Step 3 and Step 4.
                            These files are named as "lexicon_CONTENT_with_keywords.txt"
                    -   Step 6: I used the script named as "create_lexicons.py" which helped my to extraxt all the keywords(Bankası, Üniversitesi, Bey etc.) from each file.
                            These files are named as "lexicon_CONTENT.txt"

            -   I created a script which named as "enamex_cleaner.py", helped me to clear the enamax tagged documents in order to test my NER.

            -   I created a script which named as "find_line.py", This script helped me to find a keyword in lexicon.
                    Example: I found unrelated word in "lexicon_person.txt" but it is hard to find it my cmd+f or eye. So this script gives me the line number.

    -   Keywords that I used to create lexicons are listed under "Keywords" folder. I used 13 keyword files in order the use in my regex.
            -   Whenever I see a general prefix or suffix, I added to releated keyword file. All of keyword files are filled by hand.


#### Regex Descriptions:
    I limited the repetitions with 6 consecutive words in order to prevent Catastrophic backtracking.
    At first a particular line searched keywords, Afterwards searched again with lexicons.
    Searching order for both keywords and lexicon is: Organization -> Location -> Time -> Person

    Organization:
        I used these regex with keywords:
            1: "(?<=" + pre_organization + r" )(\s*([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*|ve)){1,6}"
                This regex catchs organizations which are like "rakibi Arçelik" where pre_organization is rakibi.
                Organizations could have "ve" between capital words.

            2: "(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*|ve)\s*){1,6}(?=([']\w*\s*)? " + after_organization + r"\w*)"
                This regex catchs organizations which are like "Galatasarayın Başkanı" where after_organization is "Başkanı" so I do not include "Başkanı" in my catched word.
                Organizations could have "ve" between capital words.

            3: "(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]+|ve)\s*){1,6}( "+after_organization+r"\w*)"
                This regex catchs organizations which are like "Sabanci Üniversitesi" where after_organization is "Üniversite" so I include "Üniversite" in my catched word.
                Organizations could have "ve" between capital words.

        I used these regex with lexicon:
            1: "([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)"
                This regex catch all capitalized words to search in lexicon

            2:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)+"
                This regex catchs all consecutive capitalized sentences to search in lexicon.

            3: "(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)|(ve\s*))+"
                This regex catchs all consecutive capitalized sentences which could include "ve" to search in lexicon.

            4:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\.( )?)"
                This regex catchs all capitalized character which continues with "." to search in lexicon

        After every regex operation if there are still tokes with all capitals and lenght of 3:
            1: " ([A-ZÇĞİÖŞÜ]){3}(?= |'|/')"
                I do not check if catched token is really organization because most of 3 letter uppercased tokens are organizations. This regex catchs tokens like "YÖK".


    Location:
        I used these regex with keyword:
            1: "(?<=" + preLocation + r" )(\s*([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)){1,6}"
                This regex catchs locations which are like "Başkent Ankara" where preLocation is "Başkent" so I do not include "Başkent" in my catched word.

            2: "(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)\s*){1,6}(?=([']\w*\s*)? " + after_location + r"\w*)"
                This regex catchs locations which are like "İstanbul ilçesi" where after_location is "ilçe" so I do not include "ilçe" in my catched word.

            3: "(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)\s*){1,6}( " + after_location + r"\w*)"
                This regex catchs locations which are like "İstanbul Havaalanı" where after_location is "Havaalanı" so I include "Havaalanı" in my catched word.

        I used these regex with lexicon:
            1: "([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)"
                This regex catch all capitalized words to search in lexicon

            2:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)+"
                This regex catchs all consecutive capitalized sentences to search in lexicon.

            3:"(([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)|(ve\s*))+"
                This regex catchs all consecutive capitalized sentences which could include "ve" to search in lexicon.

            4:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\.( )?)"
                This regex catchs all capitalized character which continues with "." to search in lexicon


    Time:
        1:  "(\d{1,4} )?("+month+r")( \d{1,4})?"
            This regex catchs times which are like "23 Ekim 1998" where month is "Ekim" so I catched whole date.

        2:  "(( )?((-|(\d{1,4}))( )?)*)?("+month+r")"
            This regex catchs times which are like "7 - 8 Ekim" where month is "Ekim" so I catched more than one date.

        3:  "(" + preDate + r"([']\w*)? )(\d{1,4})([']\w*)?"
            This regex catchs times which are like "M.O. 500" where preDate is "M.O." so I catched all date.

        4:  "(\d{1,4} )(?=([']\w*)? "+afterDate+r"\w*)"
            This regex catchs times which are like "1998 yılı" where afterDate is "yılı" so I catched only the date.

        5:  "(" + preTime + r" )(([0-2][0-3])|[0-9])([:.]([0-5][0-9]))?"
            This regex catchs times which are like "saat 5" where preTime is "saat"

        6:  "\d{2}[./-]\d{2}[./-]\d{2,4}"
            This regex catchs times which are like "01.01.2000".

        7:  "(([A-Z]+)|\d+)(. yüzyıl)"
            This regex catchs times which are like "5. yüzyıl" or "V. yüzyıl".

        8:  "(([0-2][0-3])|[0-9])[:.]([0-5][0-9])"
            This regex catchs times which are like "23:59"

        9:  "([12][0-9]{3})(?=[']\w*)?"
            This regex catchs times which are like "1997"


    Person:
        I used these regex with keyword:
            1:  "(?<=" + prePerson + r" )(\s*[A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*){1,6}"
                This regex catchs person names which are like "sayın Cavit" where prePerson is "sayın" so I do not include "sayın" in my catched word.

            2:  "(" + r"(III\.|I\.|II\.|IV\.|V\.|VI\.)" + r" )(\s*[A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*){1,6}"
                This regex catchs person names which are like "V. Cavit".

            3:  "([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*){1,6}(?=([']\w*)? " + afterPerson + r"\w*)"
                This regex catchs person names which are like "Cavit Bey" where afterPerson is "Bey" so I do not include "Bey" in my catched word.

        I used these regex with lexicon:
            1:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*)"
                This regex catch all capitalized words to search in lexicon

            2:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\s*)+"
                This regex catchs all consecutive capitalized sentences to search in lexicon.

            3:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*((')|\s*))+"
                This regex catchs all consecutive capitalized sentences with "'" to search in lexicon.

            4:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*[']?)+"
                This regex catchs all consecutive capitalized sentences which seperated by "'" to search in lexicon.

            5:"([A-ZÇĞİÖŞÜ]+[a-zçğıöşü]*\.( )?)"
                This regex catchs all capitalized character which continues with "." to search in lexicon
