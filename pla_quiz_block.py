import random

QUIZ_DATA = [

    # ── ORGANIZATIONAL STRUCTURE ──────────────────────────────
    {
        "section": "Organizational Structure",
        "question": "Which CMC organization, along with its grade, appears first in protocol order among the 15 CMC organizations?",
        "options": {
            "A": "The Political Work Department, Theater Command Leader grade",
            "B": "Joint Staff Department, Theater Command Leader grade",
            "C": "General Office, Theater Command Deputy Leader grade",
        },
        "answer": "C",
        "explanation": (
            "The 15 CMC organizations in protocol order:\n\n"
            "1. General Office (TC Deputy Leader)\n"
            "2. Joint Staff Department (TC Leader)\n"
            "3. Political Work Department (TC Leader)\n"
            "4. Logistic Support Department (TC Leader)\n"
            "5. Equipment Development Department (TC Leader)\n"
            "6. Training Management Department (TC Deputy Leader)\n"
            "7. National Defense Mobilization Department (TC Deputy Leader)\n"
            "8. Discipline Inspection Commission (TC Leader)\n"
            "9. Politics and Law Commission (TC Deputy Leader)\n"
            "10. Science and Technology Commission (TC Deputy Leader)\n"
            "11. Office for Strategic Planning (Corps Leader)\n"
            "12. Office for Reform and Organizational Structure (Corps Leader)\n"
            "13. Office for International Military Cooperation (Corps Leader)\n"
            "14. Audit Office (Corps Leader)\n"
            "15. Agency for Offices Administration (Corps Leader)\n\n"
            "The CMC General Office is always listed first in protocol order. It processes all CMC "
            "communications and documents, coordinates meetings, and conveys orders and directives "
            "to other CMC subordinate functional sections. The General Office is the CMC's lead "
            "administrative organization and is routinely involved in issuing policies and other "
            "documents that dictate how the PLA should function. Tangentially, the CMC General "
            "Office also pursues counter-espionage efforts with the PRC's Ministry of Public Security. "
            "CMC General Office leaders also accompany other PLA leaders in domestic inspections and "
            "key leader engagements with foreign leaders. Of deep significance, the CMC General "
            "Office is also led by one of Xi Jinping's closest confidants."
        ),
    },
    {
        "section": "Organizational Structure",
        "question": "How many Theater Commands (TCs) are there, and what is their protocol order?",
        "options": {
            "A": "5 TCs: Eastern, Southern, Western, Northern, and Central",
            "B": "7 TCs: Shenyang, Beijing, Lanzhou, Jinan, Nanjing, Guangzhou, and Chengdu",
            "C": "3 TCs: Northern, Eastern, and Southern",
        },
        "answer": "A",
        "explanation": (
            "In February 2016, as part of the 'Deepen National Defense and Military Reforms' "
            "(深化国防和军队改革), the PLA transitioned from seven Military Regions (in protocol order: "
            "Shenyang, Beijing, Lanzhou, Jinan, Nanjing, Guangzhou, and Chengdu) into five Theater "
            "Commands listed in protocol order as: Eastern Theater Command (ETC) (东部战区), Southern "
            "Theater Command (STC) (南部战区), Western Theater Command (WTC) (西部战区), Northern Theater "
            "Command (NTC) (北部战区), and Central Theater Command (CTC) (中部战区). The Lanzhou Military "
            "Region's headquarters was downgraded and transitioned onto the WTC Army's headquarters. "
            "The Jinan Military Region's headquarters was also downgraded and transitioned into the "
            "NTC Army's headquarters."
        ),
    },
    {
        "section": "Organizational Structure",
        "question": "Do the PLA's Ministry of National Defense (MND) and the U.S. Department of Defense have the same basic responsibilities?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "No. The MND's primary responsibilities are to implement foreign relations, coordinate "
            "mobilization efforts, and help manage conscription. Prior to the 2016 reorganization, "
            "every organization within the MND had its own name but each one was dual-hatted with a "
            "CMC organization and may have had a different name. However, under the reorganization, "
            "most of the organizations moved completely from the MND to the CMC, so there are "
            "virtually no dual-hatted organizations. The key MND organizations today are the General "
            "Office, the MND Information Office, and the MND Spokesperson. The MND also works closely "
            "with the CMC's Office of International Military Cooperation (OIMC), which used to be "
            "dual-hatted with the MND.\n\n"
            "The first step in understanding the roles of China's Defense Minister and the Ministry "
            "of National Defense is to recognize that they do not equate in any respect to the United "
            "States' Secretary of Defense and Department of Defense in terms of making defense policy "
            "or commanding the military. In China, the Chinese Communist Party's (CCP's) Central "
            "Military Commission (CMC/中央军委), which has had a mirror image State CMC since 1982, "
            "are responsible for making defense policy and commanding the military. The Defense "
            "Minister is the public face of MND. Although previous Defense Ministers served as a CMC "
            "member and a State Councilor, the current Defense Minister, Admiral Dong Jun, has not "
            "been added as a CMC Member or as a State Councilor as of August 2024. Therefore, the "
            "ministry, itself, is essentially an entity that exists in name only."
        ),
    },

    # ── LEADERSHIP ────────────────────────────────────────────
    {
        "section": "Leadership",
        "question": "Are commanders and political officers still co-equals if they do not have the same rank?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "A",
        "explanation": (
            "Yes, because they have the same grade. Under the current system since 1988, every PLA "
            "organization and officer is assigned one of 15 grades from platoon level to CMC to "
            "designate their position in the military hierarchy. As part of the PLA's 11th force "
            "reduction that began in 2016, the MR leader and MR deputy leader grades were renamed TC "
            "leader and deputy leader grades, respectively. Of particular note, every PLA organization "
            "is assigned a corresponding grade. Each grade from TC deputy leader down has two assigned "
            "ranks, while some ranks, such as major general, can be assigned to up to four grades. "
            "Unlike the U.S. military, which assigns numbers to grades such as O-1 to O-10, the PLA "
            "does not assign numbers to its grades except for special technical officers. On average, "
            "officers up to the rank of senior colonel are promoted in grade every three years, while "
            "they are promoted in rank approximately every four years. Rarely do personnel receive a "
            "rank and grade promotion at the same time; however, that system is slowly changing."
        ),
    },
    {
        "section": "Leadership",
        "question": "What types of Party Committees exist in the PLA?",
        "options": {
            "A": "Strategic Party Committees and Operational Party Committees",
            "B": "Unit Party Committees and Administrative/Functional Department Party Committees",
            "C": "Central Party Committees and Regional Party Committees",
        },
        "answer": "B",
        "explanation": (
            "Unit Party Committees and Administrative/Functional Department Party Committees, meaning "
            "that every department, such as the Operations Bureau and Intelligence Bureau within the "
            "Joint Staff or Staff Department, down to the regiment level has its own Party Committee."
        ),
    },
    {
        "section": "Leadership",
        "question": "Who is the secretary and deputy secretary in a Party Standing Committee?",
        "options": {
            "A": "The commander is the secretary, the chief of staff is the deputy secretary",
            "B": "The political officer is the secretary, the commander is the deputy secretary",
            "C": "The chief of staff is the secretary, the political officer is the deputy secretary",
        },
        "answer": "B",
        "explanation": (
            "The political officer is the secretary, the commander is the deputy secretary, and the "
            "deputy commanders, deputy political commissars, chief of staff, director of the Political "
            "Work Department, Secretary of the Discipline Inspection Commission, and Director of the "
            "Support Department are members. Note that the political commissar for the Support "
            "Department is not on the unit Standing Committee. Although the PLA created an enlisted "
            "Master Chief program for companies to brigades, none of them serve on a Party Standing "
            "Committee. There are no enlisted force advisors to commanders above the brigade level."
        ),
    },

    # ── LOGISTICS AND MAINTENANCE ─────────────────────────────
    {
        "section": "Logistics and Maintenance",
        "question": "What organization is the newly-created Joint Logistics Support Force (JLSF) subordinate to?",
        "options": {
            "A": "The CMC",
            "B": "The CMC Logistic Support Department",
            "C": "The Theater Command Headquarters",
        },
        "answer": "A",
        "explanation": (
            "The Support Department is replacing the two departments at the Theater Command Service "
            "HQ and below levels. As early as 2013, corps leader-grade Army Group Armies began "
            "merging their Logistics Department and Equipment Department into a single Support "
            "Department. As part of the 2016 reorganization, the PLA renamed the CMC General "
            "Logistics Department as the Logistic Support Department and renamed the General Armament "
            "Department as the Equipment Development Department. In September 2016, the CMC created "
            "the Joint Logistics Support Force to unify logistic forces at the strategic level and to "
            "improve logistics support to the PLA's five Theater Commands (TCs). As part of the "
            "reorganization, the PLA merged its Logistics Departments and Equipment Departments into "
            "a single Support Department in each of the service headquarters down to the regiment "
            "level. Although information was found for Support Departments in Army, Air Force, Rocket "
            "Force, Military District, and Garrison corps-, division, and brigade-level headquarters, "
            "no information was found concerning the PLA Navy's headquarters at those levels. The "
            "current Support Departments now provide the equipment and maintain the equipment."
        ),
    },
    {
        "section": "Logistics and Maintenance",
        "question": "How many Corps Deputy Leader-grade Joint Logistics Support Centers are subordinate to the JLSF?",
        "options": {
            "A": "1 in each Theater Command",
            "B": "2 in each Theater Command",
            "C": "3 in each Theater Command",
        },
        "answer": "A",
        "explanation": (
            "The Joint Logistics Support Force (JLSF) is a TC Deputy Leader (TCDL)-grade [副战区] "
            "organization headquartered at the Wuhan Joint Logistics Support Base [武汉联勤保障基地] and "
            "consists of a number of directly subordinate units and five Corps Deputy Leader-grade "
            "[副军级] Joint Logistics Support Centers [JLSC, 联勤保障中心], aligned to support each of "
            "the PLA's Theater Commands."
        ),
    },
    {
        "section": "Logistics and Maintenance",
        "question": "What organization is replacing the former Logistics Department and Equipment Department at the Theater Command Service HQ and below?",
        "options": {
            "A": "Support Department",
            "B": "Operations Department",
            "C": "Management Department",
        },
        "answer": "A",
        "explanation": (
            "As part of the PLA's 11th force reduction and major reorganization that began in 2016, "
            "the PLA continued to make some major changes to the logistics and equipment structures "
            "that began around 2012, when some Logistics Departments and Equipment Departments were "
            "merged into a Support Department. Since 2016, besides creating the Joint Logistics "
            "Support Force at the Theater Command level, all Logistics Departments and Equipment "
            "Departments in the service (Navy, Air Force, and Rocket Force) headquarters were merged "
            "into a single Support Department at the three Theater Command Service Army, Navy, and "
            "Air Force Headquarters and below for all of the services and branches."
        ),
    },

    # ── EDUCATION AND TRAINING ────────────────────────────────
    {
        "section": "Education and Training",
        "question": "How many officer academic institutions have there been since 2017 (as of August 2024)?",
        "options": {
            "A": "34 institutions",
            "B": "37 institutions",
            "C": "67 institutions",
        },
        "answer": "A",
        "explanation": (
            "In 2017, the PLA reduced the number of academic institutions from 67 to 37 (34 officer "
            "universities and colleges/academies and 3 NCO schools), which included abolishing the "
            "Air Force Airborne Troop College and the Marine Corps College — the cadets now attend "
            "the Army Special Operations Academy. Several officer academic institutions have "
            "subordinate NCO schools. Non-commanding officers in all tracks receive both their cadet "
            "education and training and then return to the same institution for their post-cadet "
            "cultivation and training, where they can get a graduate degree. Commanding Officers in "
            "all tracks receive their post-cadet cultivation and training at their service Command "
            "College where they only receive a certificate. The only full-time joint cultivation and "
            "training course occurs at the National Defense University, where they also only receive "
            "a certificate, not a graduate degree."
        ),
    },
    {
        "section": "Education and Training",
        "question": "How many PLA Non-commissioned Officer (NCO) academic institutions are there?",
        "options": {
            "A": "3 institutions",
            "B": "4 institutions",
            "C": "5 institutions",
        },
        "answer": "A",
        "explanation": (
            "Concerning NCO academic institutions, the PLA did not have any NCO schools until 1986. "
            "Since then, the number has changed multiple times. Today, there are only three standalone "
            "NCO schools and several schools that are subordinate to officer academic institutions. "
            "Each NCO school is dedicated to a particular specialty. NCO schools offer only two-year "
            "secondary professional education programs/diplomas and two- to three-year post-secondary "
            "education programs/diplomas, which are roughly equivalent to a U.S. associate's degree. "
            "No NCO schools offer a bachelor's degree. The current three standalone NCO academic "
            "institutions are: 1) Naval NCO School; 2) Air Force Communication NCO Academy; and "
            "3) Rocket Force NCO School. Of note, there is no standalone Army NCO School; however, "
            "there is a Wuhan Ordnance NCO School subordinate to the Army Engineering University, "
            "an NCO school subordinate to the Army Academy of Artillery and Air Defense, and an NCO "
            "school subordinate to the Army Medical University. The Air Force has a subordinate NCO "
            "school subordinate to its Early Warning Academy, and the Rocket Force University of "
            "Engineering has a subordinate NCO school. Several officer academic institutions also "
            "offer NCO training classes."
        ),
    },
    {
        "section": "Education and Training",
        "question": "At what level do PLA academic institutions begin providing joint education for officers in different services?",
        "options": {
            "A": "Command College (company-grade officers)",
            "B": "Command College (field-grade officers)",
            "C": "National Defense University (flag officer)",
        },
        "answer": "C",
        "explanation": (
            "The National Defense University is identified as the only comprehensive joint command "
            "university for senior-level professional education in the Chinese military "
            "(中国军队高级任职教育的一所综合性联合指挥大学). As such, NDU is the PLA's only joint commanding "
            "officer academic institution, which begins at the corps level (major general)."
        ),
    },

    # ── OFFICER CORPS ─────────────────────────────────────────
    {
        "section": "Officer Corps",
        "question": "How many officer ranks and grades are there?",
        "options": {
            "A": "8 ranks and 18 grades",
            "B": "12 ranks and 10 grades",
            "C": "10 ranks and 15 grades",
        },
        "answer": "C",
        "explanation": (
            "10 ranks and 15 grades. As such, each grade has 2 ranks and some ranks can be assigned "
            "to 3-4 grades. In the PLA, ranks don't matter. Personnel do not call each other by their "
            "rank. They call them by their surname and billet — as in 'Wang Deputy Commander.' "
            "Promotions are based on the grade structure. Officers up to regiment leader grade get "
            "promoted every 3 years and receive rank promotions every 4 years."
        ),
    },
    {
        "section": "Officer Corps",
        "question": "What are the different officer career tracks?",
        "options": {
            "A": "Military/Operational Officers, Political Officers, Logistics Officers, Equipment Officers, Technical Officers",
            "B": "Command and Administrative Officers, Special Technical Officers, Staff Officers",
            "C": "Strategic Officers, Tactical Officers, Operational Officers, Support Officers, Technical Officers",
        },
        "answer": "B",
        "explanation": (
            "Prior to 2021, the PLA's officer corps, which it calls active-duty officers/cadres, was "
            "organized into five career tracks: military/operational officer, political officer, "
            "logistics officer, equipment/armament officer, and special technical officer. The PLA "
            "later combined the first four career tracks together and identified them as non-special "
            "technical officers, and in 2021 renamed them 'command and administrative officers.' It "
            "still has the special technical officer track as a separate track. Unlike the U.S. "
            "military, the PLA does not have alpha-numeric codes like the Military Occupational "
            "Specialty (MOS) for its officers or enlisted personnel.\n\n"
            "The PLA further organizes its officers into three categories, each of which receive "
            "different types of education and training as they move up the career ladder:\n\n"
            "Commanding officers (指挥军官): includes the Commander, Political Commissar, Deputy "
            "Commanders and Political Commissars, the Director and Deputy Director for all first-, "
            "second-, and third-level departments within each service headquarters, Theater Command, "
            "and subordinate units, and the leaders in each of the 15 CMC organizations.\n\n"
            "Staff officers (参谋/干事): serve in each of the four first-level departments and their "
            "subordinate second- and third-level departments, as well as the 15 CMC organizations.\n\n"
            "Special technical (专业技术) officers."
        ),
    },
    {
        "section": "Officer Corps",
        "question": "How many deputy commanders do units have?",
        "options": {
            "A": "1",
            "B": "2 to 4",
            "C": "Always 3",
        },
        "answer": "B",
        "explanation": (
            "From 2 to 4, depending on the level. Never say 'the deputy commander' — always say "
            "'one of the deputy commanders.'\n\n"
            "\"Each MR commander shares responsibility with a political commissar (both are military "
            "region leader grade officers). The commander is assisted by three to five Army deputy "
            "commanders (who are military region deputy leader grade officers), the regional air "
            "force commander (dual-hatted as an MR deputy commander), and a naval fleet commander "
            "in the Jinan, Nanjing, and Guangzhou MRs (also dual-hatted as an MR deputy commander). "
            "Army deputy commanders each are assigned individual portfolios, such as operations, "
            "logistics, or armament. The MR political commissar is assisted by two or three deputy "
            "political commissars. These personnel form the nucleus of the MR-level party committee "
            "with the political commissar normally acting as first secretary.\"\n\n"
            "\"The TC headquarters' leadership consists of a commander, a political commissar, "
            "multiple deputy commanders (often two to four), and multiple deputy political commissars "
            "(DPC). Deputy commanders can serve in a single-hatted or dual-hatted capacity. "
            "Typically, there are permanent PLAA, PLAN and PLAAF deputy commanders who serve as a "
            "deputy commander in a single-hatted capacity within TC headquarters. Each TC service "
            "component (e.g. TC Army, TC Navy, TC Air Force) commander is also concurrently a TC "
            "deputy commander.\""
        ),
    },

    # ── DOCTRINE ──────────────────────────────────────────────
    {
        "section": "Doctrine",
        "question": "When was the last version of the publication Science of Military Strategy published?",
        "options": {
            "A": "2001",
            "B": "2013",
            "C": "2020",
        },
        "answer": "C",
        "explanation": (
            "The August 2020 version of The Science of Military Strategy is a revision of the "
            "previous 2017 version. The PLA's National Defense University publication is a core "
            "textbook for senior officers on how wars should be planned and conducted at the strategic "
            "level. In 2005, the PLA published an English translation of the 2001 Chinese version. "
            "In January 2022, the China Aerospace Studies Institute published an English translation "
            "of the August 2020 version using an automated translation engine. That version is "
            "available at CASI's website."
        ),
    },
    {
        "section": "Doctrine",
        "question": "What concept is the basis for China's military strategy?",
        "options": {
            "A": "The PRC's military strategy is based on the concept of 'active defense'",
            "B": "The concept of 'Peoples' War' is the basis for China's military strategy",
            "C": "The basis of the PRC's military strategy is to 'Fight Wars Under Informationized Conditions'",
        },
        "answer": "A",
        "explanation": (
            "Since 2022, the PRC's stated defense policy has been oriented toward safeguarding its "
            "sovereignty, security, and development interests, while emphasizing a greater global "
            "role for itself. The PRC's military strategy remains based on the concept of "
            "'active defense.'"
        ),
    },
    {
        "section": "Doctrine",
        "question": "The authoritative text the PLA uses to define military terms — which also includes an English translation of each Chinese term — is:",
        "options": {
            "A": "Junyu (军语 / Military Terminology)",
            "B": "Han-Ying/Ying-Han Junshi Dazidian (汉英英汉军事大字典)",
            "C": "Wubeizhi (武备字 / Chinese Military Encyclopedia)",
        },
        "answer": "A",
        "explanation": (
            "Junyu is the official military dictionary of the PLA, approved by the Central Military "
            "Commission. It is organized in 26 categories, plus 9 secondary categories under the "
            "category Army (陆军). It has 8,587 entries and 195 pictures or charts. Each entry has "
            "an English translation of the headword. It has an index of entries organized by pinyin "
            "and an English index as well. This book is the authoritative source for the current "
            "Chinese definition of military terms in the PLA. Wubeizhi is an encyclopedia of ancient "
            "Chinese military terms. Han-Ying/Ying-Han Junshi Dazidian (Chinese-English/English-"
            "Chinese Military Dictionary) is not an official publication of the PLA and does not "
            "include definitions of military terms."
        ),
    },
    {
        "section": "Doctrine",
        "question": "What is the national strategy of the People's Republic of China?",
        "options": {
            "A": "To adopt Xi Jinping's thoughts for China to resume its rightful place in the world",
            "B": "To achieve 'the great rejuvenation of the Chinese nation' by 2049",
            "C": "To 'hide capabilities and bide time' (韬光养晦 / Tao Guang Yang Hui)",
        },
        "answer": "B",
        "explanation": (
            "The strategy to achieve 'the great rejuvenation of the Chinese nation' is a determined "
            "pursuit of political, social, and military modernity to expand the PRC's national power, "
            "perfect its governance, and revise the international order in support of the PRC's "
            "system of governance and national interests. 'Hide capabilities and bide time' "
            "(Tao Guang Yang Hui) is a component of China's previous strategy."
        ),
    },

    # ── ENLISTED FORCE ────────────────────────────────────────
    {
        "section": "Enlisted Force",
        "question": "How many years do enlisted conscripts/new recruits serve at least?",
        "options": {
            "A": "2 years",
            "B": "3 years",
            "C": "4 years",
        },
        "answer": "A",
        "explanation": (
            "Prior to 1999, Army conscripts served for 3 years, while Navy, Air Force, and Second "
            "Artillery conscripts served for 4 years. After that period, they could remain on active "
            "duty for a total of 16 years before they were demobilized and sent back to their "
            "hometown. Since 1999, all conscripts serve for 2 years with the option for serving as "
            "an NCO through six grades for a total of 30 years depending on their specialty. For "
            "example, cooks and drivers have a 12-year limit. NCOs can only retire when they have "
            "served a full 30 years or reach age 55; otherwise, they are demobilized and sent home."
        ),
    },
    {
        "section": "Enlisted Force",
        "question": "How many NCO grade levels and ranks are there in the PLA?",
        "options": {
            "A": "4 grade levels and 6 ranks",
            "B": "5 grade levels and 5 ranks",
            "C": "3 grade levels and 8 ranks",
        },
        "answer": "C",
        "explanation": (
            "NCOs are organized into 3 grade levels (junior, intermediate, and senior) and 8 ranks.\n\n"
            "\"In December 2009, the CMC implemented a new 'Plan for Reforming the NCO System' along "
            "with three revised regulations which covered NCO active-duty service periods, management, "
            "and education and training. The 2009 plan and revised regulations also changed the name "
            "for each of the ranks, as well as adding a third rank at the senior NCO grade level. "
            "The plan and revised regulations allow NCOs to serve for more than a total of 14 years "
            "in the senior NCO grade level. However, the exact number of years for each rank in the "
            "senior grade level is still not clear. Unlike the officer corps, which has 15 grades and "
            "10 ranks, the enlisted force has only three NCO grade levels and a total of eight NCO "
            "ranks as shown in the table below. It is important to note that, unlike officers who "
            "wear ribbons that identify their grade and number of years served, NCOs do not wear any "
            "ribbons. In 2022, the PLA made further adjustments to the rank structure by changing "
            "the name for two ranks.\""
        ),
    },
    {
        "section": "Enlisted Force",
        "question": "Is there a central promotion board for all personnel?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "No. All officer and enlisted promotions below the corps level are done locally by the "
            "next higher level Party Committee. Specifically, platoon, company, and battalion "
            "promotions are done by the regiment Party Committee; regiment promotions by the division "
            "Party Committee; and division and brigade promotions by the corps Party Committee."
        ),
    },

    # ── FOREIGN RELATIONS ─────────────────────────────────────
    {
        "section": "Foreign Relations",
        "question": "What organization manages the PLA's foreign relations (military diplomacy)?",
        "options": {
            "A": "The Ministry of National Defense",
            "B": "The CMC Joint Staff Department's Office of International Military Cooperation",
            "C": "Both the Ministry of National Defense and the CMC Joint Staff Department's Office of International Military Cooperation",
        },
        "answer": "C",
        "explanation": (
            "The Office for International Military Coordination (OIMC / 国际军事合作办公室) was established "
            "in its current form with the 2016 reforms and is listed 13th in protocol order within "
            "the Central Military Commission (CMC). Its predecessor, the Foreign Affairs Office "
            "(FAO / 外事办公室 / 外办), was shared with the General Staff Department (GSD / 参谋总部), "
            "reflecting its dual mission of foreign representation and foreign operations, primarily "
            "intelligence and information operations. This dual alignment continued after the reforms, "
            "with the OIMC being elevated to a direct subordinate of the CMC, maintaining its 13th "
            "place in protocol order and receiving the grade of corps leader, along with its own "
            "shoulder patch. Currently, the OIMC is tasked with developing and executing military "
            "cooperation in the New Era, guided by the 'Regulations on International Military "
            "Cooperation' (国际军事合作工作条例), which came into force on March 1, 2021, and informed "
            "by the 2019 White Paper, 'China's National Defense in the New Era.' The official "
            "Ministry of National Defense (MND) website defines the OIMC as, 'The office ... mainly "
            "responsible for foreign military exchanges and cooperation, and for managing and "
            "coordinating the foreign affairs work of the whole military.'"
        ),
    },
    {
        "section": "Foreign Relations",
        "question": "How often has the PLA Navy sent 3-ship escort task forces to the Gulf of Aden since 2008 for anti-piracy missions?",
        "options": {
            "A": "2 per year",
            "B": "3 per year",
            "C": "4 per year",
        },
        "answer": "C",
        "explanation": (
            "According to China's Ministry of National Defense, as of December 2023, the PLAN had "
            "dispatched more than 150 ships and over 35,000 troops in 45 anti-piracy escort task "
            "forces (ETF) to the Gulf of Aden and adjacent waters since 2008 — approximately 4 per "
            "year. According to Global Times, 'After an escort task force completes an escort mission "
            "in the Gulf of Aden, it usually conducts a two-month foreign visit, during which it "
            "will conduct joint exercises with foreign navies. Through this way, the PLA Navy "
            "displays its image of being a civilized and peaceful force.'"
        ),
    },
    {
        "section": "Foreign Relations",
        "question": "Which service has conducted the most military exercises with foreign countries since 2018 (as of June 2024)?",
        "options": {
            "A": "Army",
            "B": "Navy",
            "C": "Air Force",
        },
        "answer": "A",
        "explanation": (
            "In 2023, China participated in 24 joint military exercises, a significant increase from "
            "the COVID period, yet still below 2018 and 2019 levels.\n\n"
            "Joint Military Exercises by Service, 2018-2023:\n"
            "Navy:       13 | 12 | 1 | 6 | 4 | 10  (Total: 46)\n"
            "Army:       16 | 22 | 5 | 7 | 2 |  7  (Total: 59)\n"
            "Air Force:   3 |  4 | 2 | 1 | 3 |  4  (Total: 17)\n\n"
            "In 2023, the Navy witnessed a resurgence in exercise participation, increasing from 4 "
            "to 10 exercises and surpassing the Army in that year, showcasing a revitalized focus "
            "on maritime operations. However, the Army leads the full 2018-2023 period overall. "
            "There was a notable increase in joint exercises in Southeast Asia in 2023 (14 exercises "
            "vs. 2 the prior year). Engagement with Russia remained consistent at 5 exercises. "
            "Exercises with South Asia declined due to China-India tensions, leaving Pakistan as the "
            "only South Asian partner since 2020."
        ),
    },

    # ── QUALITY OF LIFE ───────────────────────────────────────
    {
        "section": "Quality of Life",
        "question": "At what age can military male and female personnel get married?",
        "options": {
            "A": "Anytime",
            "B": "Age 21 for both males and females",
            "C": "Age 25 for males and age 23 for females",
        },
        "answer": "C",
        "explanation": (
            "Males must be at least 25 years old and females 23. Unmarried personnel cannot live "
            "together. Late marriage is encouraged. Two-year conscripts/enlistees are not allowed "
            "to marry. Personnel who are 30 years or older can receive help from the unit in "
            "matchmaking."
        ),
    },
    {
        "section": "Quality of Life",
        "question": "What personnel do units provide matchmaking ceremonies for if they are 30 years old and not married?",
        "options": {
            "A": "Males",
            "B": "Females",
            "C": "Males and Females",
        },
        "answer": "A",
        "explanation": (
            "The PLA works tirelessly to organize matchmaking events and group weddings to help "
            "military personnel find spouses, because not being able to find wives has become a "
            "major concern and has prompted more marriage-age military members to leave the military "
            "or not want to join in the first place."
        ),
    },
    {
        "section": "Quality of Life",
        "question": "Can two-year conscripts live off base?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "The PLA requires all two-year conscripts/enlistees to live in on-base military barracks. "
            "As conscripts cannot get married, they are not allowed to live off base. NCOs who were "
            "below Master Sergeant Class Four (less than 10 years of service) are also required to "
            "live in barracks. Senior Grade NCOs, upon approval for their family to accompany the "
            "military member, will be provided housing with the military member paying a monthly "
            "rent. Active-duty NCOs also receive rent allowance."
        ),
    },

    # ── WEAPON SYSTEMS AND EQUIPMENT ──────────────────────────
    {
        "section": "Weapon Systems and Equipment",
        "question": "The PRC's Military-Civil Fusion (MCF) strategy includes objectives to:",
        "options": {
            "A": "Increase the lethality and precision of current key weapons systems, particularly tactical delivery systems and munitions",
            "B": "Develop and acquire advanced multiservice-use technology for military and civilian purposes and deepen reform of national civilian and defense educational institutions",
            "C": "Develop and acquire advanced dual-use technology for military purposes and deepen reform of the national defense science and technology industries",
        },
        "answer": "C",
        "explanation": (
            "The PRC's MCF development strategy encompasses six interrelated efforts: (1) fusing "
            "China's defense industrial base to its civilian technology and industrial base; "
            "(2) integrating and leveraging science and technology innovations across military and "
            "civilian sectors; (3) cultivating talent and blending military and civilian expertise "
            "and knowledge; (4) building military requirements into civilian infrastructure and "
            "leveraging civilian construction for military purposes; (5) leveraging civilian service "
            "and logistics capabilities for military purposes; and (6) expanding and deepening "
            "China's national defense mobilization system to include all relevant aspects of its "
            "society and economy for use in competition and war."
        ),
    },
    {
        "section": "Weapon Systems and Equipment",
        "question": "The PRC's goals for modernizing its armed forces in the 'New Era' are:",
        "options": {
            "A": "By 2027: accelerate integrated development of mechanization, informatization, and intelligentization; By 2035: basically complete modernization of national defense; By 2049: fully transform into world-class forces",
            "B": "By 2027: develop, test, and field sufficient weapons to liberate Taiwan; By 2035: basically complete modernization; By 2049: world-class forces",
            "C": "By 2027: develop weapons for Taiwan; By 2040: complete modernization; By 2059: world-class forces",
        },
        "answer": "A",
        "explanation": (
            "In a March 2021 speech, Xi Jinping detailed that the 2027 modernization goal is the "
            "first step in a broader modernization effort. PLA writings note the 'three-step' "
            "modernization plan connects 'near-, medium-, and long-term goals in 2027, 2035, and "
            "2049' respectively.\n\n"
            "By 2027: 'Accelerate the integrated development of mechanization, informatization, and "
            "intelligentization,' while boosting the speed of modernization in military theories, "
            "organizations, personnel, and weapons and equipment.\n\n"
            "By 2035: 'To comprehensively advance the modernization of military theory, "
            "organizational structure, military personnel, and weaponry and equipment in step with "
            "the modernization of the country and basically complete the modernization of national "
            "defense and the military.'\n\n"
            "By 2049: 'To fully transform the people's armed forces into world-class forces.'"
        ),
    },
    {
        "section": "Weapon Systems and Equipment",
        "question": "Which of the following statements about PLAAF and PLAN Aviation aircraft is true?",
        "options": {
            "A": "PLAAF and PLAN Aviation continue to field greater numbers of fifth-generation aircraft and probably will become a majority fifth-generation force within the next several years",
            "B": "PLAAF, PLAA, and PLAN Aviation continue to field greater numbers of fourth-generation aircraft and probably will become a majority fifth-generation force within the next decade",
            "C": "PLAAF and PLAN Aviation continue to field greater numbers of fourth-generation aircraft and probably will become a majority fourth-generation force within the next several years",
        },
        "answer": "C",
        "explanation": (
            "As of 2023, more than 1,300 of 1,900 total fighters (not including trainers) are "
            "fourth-generation. For fifth-generation fighters, the PLAAF has operationally fielded "
            "its new J-20 fifth-generation stealth fighter, and PRC social media revealed a new "
            "2-seat variant of the J-20 in October 2021. However, the overall force remains "
            "predominantly fourth-generation and is trending toward becoming a majority "
            "fourth-generation force within the next several years — not fifth-generation."
        ),
    },
]


# =============================================================
# QUIZ MODE
# =============================================================

if mode == "🎯 Quiz":
    st.subheader("PLA Knowledge Assessment")
    st.markdown(
        "Test your understanding of the People's Liberation Army across eight subject areas. "
        "Questions were developed in collaboration with **Kenneth W. Allen**. "
        "Current as of **August 2024**."
    )
    st.divider()

    if "quiz_section"   not in st.session_state: st.session_state.quiz_section   = "All Sections"
    if "quiz_questions" not in st.session_state: st.session_state.quiz_questions = []
    if "quiz_index"     not in st.session_state: st.session_state.quiz_index     = 0
    if "quiz_score"     not in st.session_state: st.session_state.quiz_score     = 0
    if "quiz_answered"  not in st.session_state: st.session_state.quiz_answered  = False
    if "quiz_selected"  not in st.session_state: st.session_state.quiz_selected  = None
    if "quiz_started"   not in st.session_state: st.session_state.quiz_started   = False
    if "quiz_complete"  not in st.session_state: st.session_state.quiz_complete  = False
    if "quiz_history"   not in st.session_state: st.session_state.quiz_history   = []

    SECTIONS = ["All Sections"] + sorted(set(q["section"] for q in QUIZ_DATA))

    def start_quiz(section):
        pool = QUIZ_DATA if section == "All Sections" else [q for q in QUIZ_DATA if q["section"] == section]
        shuffled = pool.copy()
        random.shuffle(shuffled)
        st.session_state.quiz_questions = shuffled
        st.session_state.quiz_index     = 0
        st.session_state.quiz_score     = 0
        st.session_state.quiz_answered  = False
        st.session_state.quiz_selected  = None
        st.session_state.quiz_started   = True
        st.session_state.quiz_complete  = False
        st.session_state.quiz_history   = []
        st.session_state.quiz_section   = section

    if not st.session_state.quiz_started:
        col_sel, col_btn = st.columns([2, 1])
        with col_sel:
            section_choice = st.selectbox("Choose a section (or take the full quiz):", SECTIONS, key="section_selector")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("▶  Start Quiz", use_container_width=True):
                start_quiz(section_choice)
                st.rerun()
        st.divider()
        st.markdown("**Quiz sections:**")
        section_counts = {}
        for q in QUIZ_DATA:
            section_counts[q["section"]] = section_counts.get(q["section"], 0) + 1
        cols = st.columns(4)
        for i, (sec, count) in enumerate(section_counts.items()):
            cols[i % 4].metric(sec, f"{count} questions")

    elif st.session_state.quiz_complete:
        total = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        pct   = round(score / total * 100) if total else 0
        if pct == 100:  grade_msg = "🏆 Perfect score — Ken Allen would be proud."
        elif pct >= 80: grade_msg = "⭐ Strong result. You know your PLA."
        elif pct >= 60: grade_msg = "📚 Good foundation. A few areas to review."
        else:           grade_msg = "🔄 Keep studying — the PLA is complex."
        st.markdown(f"### Quiz Complete — {grade_msg}")
        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.metric("Final Score", f"{score} / {total}")
        r2.metric("Percentage",  f"{pct}%")
        r3.metric("Section",     st.session_state.quiz_section)
        st.divider()
        if st.session_state.quiz_history:
            st.markdown("**Results by section:**")
            sec_results = {}
            for item in st.session_state.quiz_history:
                s = item["section"]
                if s not in sec_results:
                    sec_results[s] = {"correct": 0, "total": 0}
                sec_results[s]["total"]   += 1
                sec_results[s]["correct"] += 1 if item["correct"] else 0
            breakdown_cols = st.columns(min(len(sec_results), 4))
            for i, (sec, res) in enumerate(sec_results.items()):
                breakdown_cols[i % 4].metric(sec, f"{res['correct']}/{res['total']}", delta=f"{round(res['correct']/res['total']*100)}%")
            st.divider()
            missed = [item for item in st.session_state.quiz_history if not item["correct"]]
            if missed:
                st.markdown(f"**Review — {len(missed)} missed question(s):**")
                for item in missed:
                    with st.expander(f"❌  {item['question'][:80]}..."):
                        st.markdown(f"**Your answer:** {item['selected']} — {item['options'][item['selected']]}")
                        st.markdown(f"**Correct answer:** {item['answer']} — {item['options'][item['answer']]}")
                        st.markdown("---")
                        st.markdown(f"**Explanation:** {item['explanation']}")
                st.divider()
        col_restart, col_new = st.columns(2)
        with col_restart:
            if st.button("🔄  Retry Same Section", use_container_width=True):
                start_quiz(st.session_state.quiz_section)
                st.rerun()
        with col_new:
            if st.button("🏠  Choose New Section", use_container_width=True):
                st.session_state.quiz_started  = False
                st.session_state.quiz_complete = False
                st.rerun()

    else:
        questions = st.session_state.quiz_questions
        idx       = st.session_state.quiz_index
        total_q   = len(questions)
        if idx >= total_q:
            st.session_state.quiz_complete = True
            st.rerun()
        q = questions[idx]
        prog_col, score_col, section_col = st.columns([4, 1, 1])
        with prog_col:
            st.progress((idx) / total_q, text=f"Question {idx + 1} of {total_q}")
        score_col.metric("Score", f"{st.session_state.quiz_score}/{idx}")
        section_col.metric("Section", q["section"].split()[0])
        st.divider()
        st.markdown(f"### {q['question']}")
        st.markdown("")
        answered = st.session_state.quiz_answered
        selected = st.session_state.quiz_selected
        for key, text in q["options"].items():
            if answered:
                if key == q["answer"]:
                    label = f"✅  {key})  {text}"
                elif key == selected and selected != q["answer"]:
                    label = f"❌  {key})  {text}"
                else:
                    label = f"　  {key})  {text}"
            else:
                label = f"{key})  {text}"
            if st.button(label, key=f"opt_{idx}_{key}", disabled=answered, use_container_width=True):
                st.session_state.quiz_selected = key
                st.session_state.quiz_answered = True
                if key == q["answer"]:
                    st.session_state.quiz_score += 1
                st.session_state.quiz_history.append({
                    "section":     q["section"],
                    "question":    q["question"],
                    "options":     q["options"],
                    "answer":      q["answer"],
                    "selected":    key,
                    "correct":     key == q["answer"],
                    "explanation": q["explanation"],
                })
                st.rerun()
        if answered:
            st.divider()
            if selected == q["answer"]:
                st.success("✅  Correct!")
            else:
                st.error(f"❌  Incorrect — the correct answer is **{q['answer']}**: {q['options'][q['answer']]}")
            with st.expander("📖  Ken Allen's Explanation", expanded=True):
                st.markdown(q["explanation"])
            st.divider()
            is_last   = (idx + 1 >= total_q)
            btn_label = "🏁  Finish Quiz" if is_last else "Next Question ▶"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.quiz_index   += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
                if idx + 1 >= total_q:
                    st.session_state.quiz_complete = True
                st.rerun()
