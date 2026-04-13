"""
Golden Dataset — No-Task Conversations
~30 conversations where conv_has_task = FALSE.

Categories:
  - Social / casual chat
  - FYI announcements (no action required)
  - Questions fully answered in-thread
  - Celebrations / kudos
  - Status reports read-only
  - Information sharing (no follow-up needed)
"""

from conversations_1on1 import m  # reuse the message helper


NOTASK_CONVERSATIONS = [

    # =========================================================================
    # NT1: Birthday Wishes (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Happy Birthday Chris! 🎂",
        "domain": "Social",
        "members": ["laurakim", "chrisevans", "ninacosta", "derekjohnson", "lisaanderson"],
        "messages": [
            m("laurakim", "Happy birthday @Chris! 🎉🎂 Hope you have an amazing day!",
              mentions=["chrisevans"],
              notes="Birthday greeting — no task"),
            m("ninacosta", "Happy birthday Chris!! 🥳 Are you doing anything fun tonight?",
              notes="Social question — no task"),
            m("chrisevans", "Thanks everyone! Yeah, going to that new Italian place downtown with some friends. Very excited. 😄",
              notes="Social response"),
            m("derekjohnson", "Oh nice, I've heard great things! Happy birthday man 🎉",
              notes="Social"),
            m("lisaanderson", "Happy birthday Chris! 🎂 Enjoy the evening!",
              notes="Social greeting"),
        ],
    },

    # =========================================================================
    # NT2: Weekend Plans (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Weekend Plans",
        "domain": "Social",
        "members": ["jameswilson", "priyasharma", "alexkumar", "ninacosta"],
        "messages": [
            m("jameswilson", "Anyone doing anything fun this weekend?",
              notes="Social question — no task"),
            m("priyasharma", "Taking the kids to the science museum. They have a new robotics exhibit that looks cool. 🤖",
              notes="Social"),
            m("alexkumar", "Nice! I'm going hiking at Rattlesnake Ridge if the weather holds up. 🏔️",
              notes="Social"),
            m("ninacosta", "I'm binge-watching that new Netflix series everyone's been talking about. Zero guilt. 😂",
              notes="Social"),
            m("jameswilson", "Ha! I might do the same honestly. The couch is calling my name.",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT3: Office Closure Announcement (FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Office Closure — Presidents' Day",
        "domain": "HR",
        "members": ["daniellebooks", "sarahmitchell", "lisaanderson", "kevinzhang"],
        "messages": [
            m("daniellebooks", "Hi all — just a reminder that the office will be closed on Monday, February 16 for Presidents' Day. No action needed, just enjoy the long weekend! 🇺🇸",
              notes="FYI announcement — no task"),
            m("sarahmitchell", "Thanks for the reminder, Danielle!",
              notes="Acknowledgment"),
            m("lisaanderson", "Perfect timing — my PTO request for Tuesday is already in so I get a 4-day weekend 😊",
              notes="Social"),
            m("kevinzhang", "Noted, thanks!",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # NT4: System Maintenance Completed (FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "System Maintenance — Complete",
        "domain": "Engineering",
        "members": ["alexkumar", "jameswilson", "priyasharma", "derekjohnson"],
        "messages": [
            m("alexkumar", "FYI — the scheduled maintenance window for the production database is now complete. All services are back online and running normally. No issues detected during the migration.",
              notes="FYI — maintenance completed, no action needed"),
            m("jameswilson", "Great, monitoring looks clean on my end too. Latency is actually slightly better than before.",
              notes="Status confirmation — resolved"),
            m("priyasharma", "Awesome. API response times are looking good in Grafana. Nice work team! 👏",
              notes="Appreciation — no task"),
            m("derekjohnson", "Thanks for the update Alex. I'll let the customers who asked about it know.",
              notes="Acknowledgment — Derek's action is self-initiated, trivial"),
        ],
    },

    # =========================================================================
    # NT5: Team Achievement Celebration (Celebration)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "We Hit 10K Customers! 🎉",
        "domain": "Sales",
        "members": ["michaelchen", "sofiaramirez", "sarahmitchell", "laurakim", "racheltorres"],
        "messages": [
            m("michaelchen", "Team — I'm thrilled to share that we officially crossed 10,000 active customers this morning! 🎉🔥 This is a huge milestone for EcoSync.",
              is_important=True,
              notes="Milestone announcement — Important but no task"),
            m("sofiaramirez", "Amazing!! The sales team has been crushing it. So proud of everyone. 🙌",
              notes="Celebration"),
            m("sarahmitchell", "Incredible achievement. This took 18 months of hard work from every single department. I'm buying lunch for the whole office on Friday. 🍕",
              notes="Celebration + informal gesture"),
            m("laurakim", "We should do a social media post about this! Oh wait, it went out at 9 AM — already on LinkedIn and Twitter 😄",
              notes="Self-resolved — social media already handled"),
            m("racheltorres", "From a finance perspective, this puts us solidly on track for our Series B targets. Well done everyone! 📈",
              notes="FYI — finance context"),
        ],
    },

    # =========================================================================
    # NT6: Lunch Order (Resolved In-Thread)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Lunch Today",
        "domain": "Social",
        "members": ["lisaanderson", "kevinzhang", "ninacosta", "derekjohnson"],
        "messages": [
            m("lisaanderson", "Hey! Anyone want to go halfsies on the Thai place for lunch? Their pad thai is 🔥",
              notes="Social coordination — no task"),
            m("kevinzhang", "I'm in! Green curry for me please. 🍛",
              notes="Social"),
            m("ninacosta", "Yes! Pad see ew please. Should I place the order?",
              notes="Volunteer — immediately acted on"),
            m("derekjohnson", "Mango sticky rice for me. Dessert counts as lunch, right? 😂",
              notes="Social"),
            m("ninacosta", "Order placed! Should be here by 12:30. I added mango sticky rice for the table. 🥭",
              notes="Action completed in-thread"),
            m("lisaanderson", "You're the best Nina! 🙏",
              notes="Thanks"),
        ],
    },

    # =========================================================================
    # NT7: How-To Question Answered (Resolved Q&A)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "VPN Setup Help",
        "domain": "IT",
        "members": ["ninacosta", "jameswilson"],
        "messages": [
            m("ninacosta", "Hey James, quick question — how do I connect to the staging VPN from my new laptop? The old instructions don't seem to work anymore.",
              notes="Question — answered in thread"),
            m("jameswilson", "Yeah, we switched VPN providers last month. Go to vpn.meridian.io, download the new client, and use your Okta SSO credentials. Let me know if it doesn't work.",
              notes="Answer provided"),
            m("ninacosta", "That worked perfectly, thanks! Connected in 30 seconds. Way faster than the old one. 👍",
              notes="Resolved — no outstanding work"),
        ],
    },

    # =========================================================================
    # NT8: Process Question Answered (Resolved Q&A)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Expense Report Question",
        "domain": "Finance",
        "members": ["chrisevans", "kevinzhang"],
        "messages": [
            m("chrisevans", "Hey Kevin, what's the limit for client meals before I need VP approval?",
              notes="Question — answered in thread"),
            m("kevinzhang", "It's $250 per meal for individual client meetings. Anything above that needs VP sign-off plus a business justification note. For team events it's $75 per head.",
              notes="Answer provided"),
            m("chrisevans", "Perfect, the dinner I'm logging is $180 so I should be fine. Thanks for the quick answer!",
              notes="Resolved"),
            m("kevinzhang", "Yep, you're good. Just make sure to attach the receipt. 👍",
              notes="Final clarification"),
        ],
    },

    # =========================================================================
    # NT9: Article Shared (Information Sharing)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "General — Interesting Read",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "priyasharma", "jameswilson"],
        "messages": [
            m("davidpark", "Came across this great article on microservice observability patterns: https://techblog.example.com/observability-2026. Really relevant to what we're building.",
              notes="Information sharing — no task"),
            m("alexkumar", "Good find! Their approach to distributed tracing is similar to what we discussed for the monitoring dashboard.",
              notes="Discussion"),
            m("priyasharma", "The section on SLO-based alerting is interesting. We're already doing most of that with our Datadog setup.",
              notes="Commentary"),
            m("jameswilson", "Bookmarked. The log aggregation patterns in section 3 are solid.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # NT10: Sprint Report — No Actions (Status FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Sprint 46 Report — Final Numbers",
        "domain": "Engineering",
        "members": ["alexkumar", "davidpark", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Sprint 46 final numbers are in:\n\n• Velocity: 47 points (target: 45) ✅\n• Stories completed: 12/14\n• Bugs resolved: 8\n• Carryover: 2 stories (by design — deferred to next sprint)\n\nSolid sprint everyone.",
              notes="Sprint report — FYI, no action items"),
            m("davidpark", "Good numbers. The carryover items make sense given the priority shift mid-sprint. Nice work team.",
              notes="Acknowledgment"),
            m("priyasharma", "The API performance story took longer than expected but we're happy with the result — 40% latency improvement on the main endpoints.",
              notes="Context/detail"),
            m("ninacosta", "QA pass rate was 96% this sprint. Highest we've had all quarter. 💪",
              notes="Supplementary stat"),
        ],
    },

    # =========================================================================
    # NT11: Work Anniversary (Celebration)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Priya's 3-Year Anniversary! 🎉",
        "domain": "Social",
        "members": ["alexkumar", "priyasharma", "davidpark", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Everyone — today marks @Priya's 3-year anniversary at Meridian! She's been an absolute rockstar on the engineering team. Thank you for everything you do 🎉",
              mentions=["priyasharma"],
              notes="Anniversary announcement"),
            m("davidpark", "3 years! Time flies. Priya, your contributions to the platform have been transformative. Here's to many more. 🙏",
              notes="Appreciation"),
            m("jameswilson", "Congrats Priya! 🎂 Remember when we had that all-nighter during the v2 launch? We've come a long way since then 😄",
              notes="Social"),
            m("ninacosta", "Happy work anniversary Priya!! The team wouldn't be the same without you. 💐",
              notes="Social"),
            m("priyasharma", "Wow, thank you all! 🥰 These 3 years have been incredible. Best team I've ever worked with.",
              notes="Gratitude"),
        ],
    },

    # =========================================================================
    # NT12: Market News Discussion (Information)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Competitor News — Worth Knowing",
        "domain": "Sales",
        "members": ["michaelchen", "sofiaramirez", "sarahmitchell"],
        "messages": [
            m("michaelchen", "Heads up — saw that Nexus Analytics just announced they're shutting down their SMB tier. All their small business customers are looking for alternatives.",
              is_important=True,
              notes="Market intel — Important as competitive signal, but no explicit task"),
            m("sofiaramirez", "Interesting. We've already been getting inbound from a few of them this week. The pipeline team is routing them normally.",
              notes="Status — already handled"),
            m("sarahmitchell", "Good intel Michael. Glad the pipeline team is already on it.",
              notes="Acknowledgment — no new action"),
        ],
    },

    # =========================================================================
    # NT13: Customer Positive Feedback (Celebration)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Amazing Customer Feedback!",
        "domain": "Customer Support",
        "members": ["derekjohnson", "mariagonzalez", "sarahmitchell", "alexkumar"],
        "messages": [
            m("derekjohnson", "Just got off a call with Pinnacle Logistics. Their CTO said, and I quote: 'EcoSync has been the single best technology investment we've made in 5 years.' 🤩",
              notes="Customer praise — no task"),
            m("mariagonzalez", "That's so great to hear! They were really frustrated 6 months ago. The turnaround has been incredible.",
              notes="Context"),
            m("sarahmitchell", "This is exactly the kind of feedback we need to share with the board. Really validates the product strategy. 🔥",
              notes="Commentary — no action item created"),
            m("alexkumar", "The engineering team will love hearing this. Thanks for sharing Derek! 🙌",
              notes="Appreciation"),
        ],
    },

    # =========================================================================
    # NT14: Weather / Water Cooler (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "General Chat",
        "domain": "Social",
        "members": ["lisaanderson", "kevinzhang", "chrisevans", "derekjohnson"],
        "messages": [
            m("lisaanderson", "Did anyone else see the sunrise this morning? Absolutely gorgeous from the 12th floor. ☀️",
              notes="Social"),
            m("kevinzhang", "Yes! I took a photo from the parking garage. The sky was insane. 🌅",
              notes="Social"),
            m("chrisevans", "I was stuck in traffic on I-5 and somehow the sunset almost made the commute worth it. Almost. 😅",
              notes="Social"),
            m("derekjohnson", "Wait, are we getting another heat wave this week? I saw something about 95° on Thursday.",
              notes="Social question"),
            m("lisaanderson", "Yeah, looks like it. Time to bring the desk fan back. 😂",
              notes="Social response"),
        ],
    },

    # =========================================================================
    # NT15: Conference Call Dial-In (Information Resolved)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Meeting Link",
        "domain": "Operations",
        "members": ["racheltorres", "kevinzhang"],
        "messages": [
            m("racheltorres", "Kevin, do you have the Teams link for the finance review? I can't find the invite.",
              notes="Question — answered in thread"),
            m("kevinzhang", "Here you go: https://teams.microsoft.com/l/meetup-join/abc123. It's also on the shared Finance calendar if you need it again.",
              notes="Answer provided"),
            m("racheltorres", "Got it, thanks! Joining now.",
              notes="Resolved"),
        ],
    },

    # =========================================================================
    # NT16: Training Session Feedback (Resolved Discussion)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Feedback on Security Training",
        "domain": "IT",
        "members": ["alexkumar", "jameswilson", "priyasharma", "ninacosta", "amandafoster"],
        "messages": [
            m("amandafoster", "Thanks everyone for completing the annual security awareness training! We had 100% completion rate this quarter. 🎉",
              notes="FYI — training complete"),
            m("alexkumar", "The phishing simulation section was actually really well done this year. Much better than last year's.",
              notes="Feedback"),
            m("jameswilson", "Agreed. The interactive scenarios were engaging. The password hygiene module could use an update though — it still references 90-day rotation which we don't do anymore.",
              notes="Feedback — informational observation"),
            m("priyasharma", "Same feedback here. Also the section on OAuth token handling was really helpful for the dev team.",
              notes="Feedback"),
            m("amandafoster", "Great feedback on the password module — I'll pass that to the vendor. Thanks everyone for the quick turnaround! 🙏",
              notes="Amanda's vendor note is her own initiative, trivial — no task created"),
        ],
    },

    # =========================================================================
    # NT17: New Office Photos (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "New Office Tour 📸",
        "domain": "Social",
        "members": ["lisaanderson", "daniellebooks", "chrisevans", "ninacosta"],
        "messages": [
            m("lisaanderson", "Just finished setting up the new collaboration space on the 4th floor! Here are some photos. The standing desks arrived and the whiteboard wall looks amazing.",
              notes="Information sharing — no task"),
            m("daniellebooks", "Wow, that looks incredible! The natural lighting is so much better than the old space.",
              notes="Appreciation"),
            m("chrisevans", "Love the whiteboard wall! Is there a booking system for the space or is it first-come?",
              notes="Question"),
            m("lisaanderson", "First-come for now. If it gets too crowded we'll add a booking sheet at the door.",
              notes="Answer — resolved"),
            m("ninacosta", "This is so nice! Can't wait to use it. 🙌",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT18: Revenue Update — Read Only (Status FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q1 Revenue — Final Numbers",
        "domain": "Finance",
        "members": ["racheltorres", "sarahmitchell", "michaelchen", "kevinzhang"],
        "messages": [
            m("racheltorres", "Q1 revenue is finalized: $18.4M, which is 12% above target. Gross margin came in at 72%. Full report is in the shared Finance folder for anyone who wants the breakdown.",
              is_important=True,
              notes="Revenue announcement — Important business signal but no task"),
            m("sarahmitchell", "Excellent result. The team should be proud. 12% above target with improving margins — that's exactly what the board wants to see.",
              notes="Commentary"),
            m("michaelchen", "Sales team delivered $6.2M in new ARR. Renewals at 94%. Strong quarter all around.",
              notes="Additional context"),
            m("kevinzhang", "Numbers all reconciled on my end. Clean close this quarter. 👍",
              notes="Confirmation"),
        ],
    },

    # =========================================================================
    # NT19: Pet Photos (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Pet Tax Thread 🐕",
        "domain": "Social",
        "members": ["ninacosta", "priyasharma", "chrisevans", "derekjohnson", "laurakim"],
        "messages": [
            m("ninacosta", "OK it's pet tax time. Here's my new puppy, Luna! 🐶 She's a 4-month-old golden retriever and she's already stolen my heart.",
              notes="Social"),
            m("priyasharma", "Oh my GOD she is adorable! 😍 Here's my cat Mochi being dramatic as usual.",
              notes="Social"),
            m("chrisevans", "Luna is so cute! And Priya, Mochi looks like she owns the place 😂",
              notes="Social"),
            m("derekjohnson", "My dog Max says hi to Luna 🐕 He's a 3-year-old lab. They'd be best friends.",
              notes="Social"),
            m("laurakim", "I don't have a pet but I volunteer at the local shelter on weekends. Yesterday I got to cuddle with 6 kittens. 🐱",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT20: Meeting Notes — FYI Only (No Action Items)
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Product Demo — Internal Preview",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "priyasharma", "ninacosta"],
        "messages": [
            m("alexkumar", "Notes from today's demo session:\n\n1. New analytics dashboard — performance is excellent, sub-200ms for all queries\n2. AI recommendation engine — accuracy improved to 94% with latest model\n3. Mobile app redesign — iOS version looking polished\n\nAll items are on track for Sprint 48.",
              notes="Meeting notes — FYI, no action items"),
            m("davidpark", "Great demo everyone. The AI recommendation accuracy improvement is impressive. Priya, well done on that.",
              notes="Praise"),
            m("priyasharma", "Thanks David! The new training data pipeline made a big difference. Excited to see it in production.",
              notes="Context"),
            m("ninacosta", "QA is tracking well too. No P0/P1 bugs open against any of these features.",
              notes="Status — confirming good state"),
        ],
    },

    # =========================================================================
    # NT21: Sports Discussion (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Did You See The Game Last Night?",
        "domain": "Social",
        "members": ["jameswilson", "derekjohnson", "michaelchen", "kevinzhang"],
        "messages": [
            m("jameswilson", "That Lakers game last night was INSANE. OT buzzer beater! 🏀",
              notes="Social"),
            m("derekjohnson", "I know! I was watching at the bar and everyone went absolutely nuts. Best game of the season.",
              notes="Social"),
            m("michaelchen", "I fell asleep in the 3rd quarter and missed everything. My timeline is full of spoilers 😭",
              notes="Social"),
            m("kevinzhang", "Classic Michael 😂 Don't worry, it'll be on YouTube highlights by now.",
              notes="Social"),
            m("jameswilson", "Playoffs are going to be wild this year. Anyone want to do a bracket pool?",
              notes="Social suggestion — no work task"),
            m("derekjohnson", "Yes! I'm in. I promise to pick terribly as always. 😅",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT22: Company All-Hands Recording (FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "All-Hands Recording Available",
        "domain": "HR",
        "members": ["daniellebooks", "sarahmitchell", "alexkumar", "michaelchen"],
        "messages": [
            m("daniellebooks", "For those who couldn't attend today's all-hands, the recording and slides are now available on SharePoint: https://meridian.sharepoint.com/allhands-q1. Passcode is MeridianQ1.",
              notes="FYI — recording shared, no task"),
            m("alexkumar", "Thanks Danielle! I was in back-to-back meetings and missed it. Will watch this afternoon.",
              notes="Acknowledgment"),
            m("michaelchen", "The Q&A section at the end was really good. Sarah addressed the remote work question directly.",
              notes="Commentary"),
        ],
    },

    # =========================================================================
    # NT23: Team Trivia (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Wednesday Trivia ⚡",
        "domain": "Social",
        "members": ["laurakim", "chrisevans", "ninacosta", "priyasharma", "derekjohnson"],
        "messages": [
            m("laurakim", "Wednesday trivia time! 🧠 What's the most spoken language in the world by total number of speakers?",
              notes="Trivia — social"),
            m("chrisevans", "Mandarin Chinese?",
              notes="Social"),
            m("ninacosta", "English!",
              notes="Social"),
            m("priyasharma", "It's English by total speakers (native + non-native). Mandarin is #1 by native speakers only.",
              notes="Social"),
            m("laurakim", "Priya is correct! 🎉 English: ~1.5 billion total speakers. Mandarin: ~1.1 billion. Next trivia on Friday!",
              notes="Social"),
            m("derekjohnson", "I was going to say Spanish but I'll take my L quietly 😂",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT24: WiFi Question Resolved (Q&A)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "WiFi Password",
        "domain": "IT",
        "members": ["derekjohnson", "lisaanderson"],
        "messages": [
            m("derekjohnson", "Lisa, what's the guest WiFi password for the conference room? We have external visitors tomorrow.",
              notes="Question — answered in thread"),
            m("lisaanderson", "It's MeridianGuest2026. It auto-rotates monthly. The current one is posted on the welcome board by reception too.",
              notes="Answer provided"),
            m("derekjohnson", "Perfect, thanks!",
              notes="Resolved"),
        ],
    },

    # =========================================================================
    # NT25: Holiday Party Recap (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Holiday Party Recap 🎄",
        "domain": "Social",
        "members": ["daniellebooks", "lisaanderson", "chrisevans", "ninacosta", "kevinzhang"],
        "messages": [
            m("daniellebooks", "Great holiday party last night! Thanks to everyone who came. 🎉 Lisa, the venue was perfect.",
              notes="Social — past event"),
            m("lisaanderson", "So much fun! The photo booth was a hit. I'll share the photos once they're uploaded. 📸",
              notes="Lisa's share is trivial/informal — not a work task"),
            m("chrisevans", "The karaoke session at the end was legendary. Kevin's rendition of Bohemian Rhapsody will live rent-free in my head forever. 😂",
              notes="Social"),
            m("kevinzhang", "I regret nothing. 🎤",
              notes="Social"),
            m("ninacosta", "It was such a great way to end the year. Already looking forward to the next one! 🥂",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT26: Git Question Answered (Q&A)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Git Branch Question",
        "domain": "Engineering",
        "members": ["ninacosta", "alexkumar"],
        "messages": [
            m("ninacosta", "Alex, which branch should I use for the regression tests? I see main, develop, and release/4.2.",
              notes="Question — answered in thread"),
            m("alexkumar", "Use develop for the regression suite. release/4.2 is frozen for the launch. Main is only for hotfixes right now.",
              notes="Answer provided"),
            m("ninacosta", "Makes sense, thanks! Targeting develop now.",
              notes="Resolved"),
        ],
    },

    # =========================================================================
    # NT27: Team Kudos (Celebration)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Shoutout — Nina's QA Work 🌟",
        "domain": "Engineering",
        "members": ["alexkumar", "ninacosta", "davidpark", "priyasharma", "jameswilson"],
        "messages": [
            m("alexkumar", "I want to give a big shoutout to @Nina for the incredible work on the automated regression suite this quarter. We went from 60% to 96% test coverage and our bug escape rate dropped by 40%. 🌟",
              mentions=["ninacosta"],
              notes="Kudos — no task"),
            m("davidpark", "Well deserved! Nina, your work has directly improved our release confidence. Thank you. 🙏",
              notes="Appreciation"),
            m("priyasharma", "The API test suite Nina built saved us during the v4.1 hotfix. We caught 3 regressions that would have gone to production. Absolute lifesaver. 💪",
              notes="Context/appreciation"),
            m("jameswilson", "+1! The infrastructure tests are solid too. Makes my deployments way less stressful 😊",
              notes="Appreciation"),
            m("ninacosta", "Thank you all so much! 🥰 This means a lot. The whole team made this possible — especially Priya for the API integration work.",
              notes="Gratitude"),
        ],
    },

    # =========================================================================
    # NT28: Product Launch Celebration (Celebration)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Meridian v4.2 Launch Day! 🚀",
        "domain": "Cross-functional",
        "members": ["sarahmitchell", "davidpark", "alexkumar", "michaelchen", "laurakim", "racheltorres"],
        "messages": [
            m("sarahmitchell", "Team — Meridian v4.2 is LIVE. 🚀 Smooth deployment, all systems green, and early customer feedback is extremely positive. Congratulations to everyone who made this happen.",
              is_important=True,
              notes="Launch announcement — Important milestone, but celebratory, no task"),
            m("davidpark", "Clean launch! Zero P0 issues in the first 4 hours. Engineering is monitoring closely but everything looks solid.",
              notes="Status update — good state"),
            m("alexkumar", "The telemetry shows 2x engagement on the new analytics features already. Incredible. 📊",
              notes="Early metrics"),
            m("michaelchen", "Sales team is already getting inbound requests. 6 new demo requests this morning alone. 🔥",
              notes="Sales impact"),
            m("laurakim", "Press coverage is rolling in — TechCrunch, VentureBeat, and The Verge all published pieces. Social engagement is 3x our usual launch numbers.",
              notes="PR results"),
            m("racheltorres", "From a financial perspective, our launch week metrics are tracking 40% above projections. Great work everyone! 🎉",
              notes="Financial context"),
        ],
    },

    # =========================================================================
    # NT29: Status Check — Everything Fine (Resolved Q&A)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Quick Status Check",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar"],
        "messages": [
            m("davidpark", "Hey Alex, how are things going with the Sprint 48 items? Just wanted to check in — no urgency.",
              notes="Status question — answered in thread"),
            m("alexkumar", "All on track. Priya finished the AI feature yesterday, James has the deployment gates 80% done, and Nina's regression suite is green. We're looking good for the sprint demo on Thursday.",
              notes="Status answer — complete"),
            m("davidpark", "Perfect, that's everything I needed to know. Thanks for the update. 👍",
              notes="Resolved — no follow-up needed"),
        ],
    },

    # =========================================================================
    # NT30: Coffee Machine Discussion (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Coffee Machine Situation ☕",
        "domain": "Social",
        "members": ["kevinzhang", "lisaanderson", "jameswilson", "chrisevans"],
        "messages": [
            m("kevinzhang", "PSA: the espresso machine on the 3rd floor is making weird noises again. I'd recommend the one on 5th floor until facilities looks at it. ☕",
              notes="FYI — informal"),
            m("lisaanderson", "Oh no, not again! That machine has a personality of its own. I already let facilities know — they're coming by this afternoon.",
              notes="Already handled — no task"),
            m("jameswilson", "The 5th floor machine makes a better latte anyway. Just saying. 😄",
              notes="Social"),
            m("chrisevans", "I've been using the pour-over setup in the marketing kitchen. Life changing. ☕✨",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT31: Commute Discussion (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Traffic Alert",
        "domain": "Social",
        "members": ["derekjohnson", "sofiaramirez", "lisaanderson", "kevinzhang"],
        "messages": [
            m("derekjohnson", "Heads up — I-405 is completely backed up. Took me 90 minutes to get in today. 😤",
              notes="FYI — informal traffic alert"),
            m("sofiaramirez", "I saw that too. There's a multi-car accident near exit 15. Took the back roads and it was fine. Try 148th Ave as an alternate.",
              notes="Advice — resolved in thread"),
            m("lisaanderson", "I lucked out and took the train today. Should I add transit info to the office Slack? We used to have that.",
              notes="Social suggestion — not a work task"),
            m("kevinzhang", "This is why I WFH on Mondays. 🏠😊",
              notes="Social"),
        ],
    },

    # =========================================================================
    # NT32: Book Club (Social)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "March Book Club Pick 📚",
        "domain": "Social",
        "members": ["priyasharma", "amandafoster", "laurakim", "daniellebooks"],
        "messages": [
            m("priyasharma", "OK team, what did everyone think of 'Project Hail Mary'? I absolutely loved it.",
              notes="Social discussion"),
            m("amandafoster", "One of the best sci-fi books I've read in years. The Rocky chapters had me tearing up. 🥺",
              notes="Social"),
            m("laurakim", "Same! I finished it in two sittings. The humor balanced the tension perfectly.",
              notes="Social"),
            m("daniellebooks", "Loved it! For April, I'm suggesting 'Klara and the Sun' by Kazuo Ishiguro. Anyone read it?",
              notes="Social"),
            m("priyasharma", "I haven't but I've heard great things. Let's do it! 📖",
              notes="Social agreement"),
        ],
    },

    # =========================================================================
    # NT33: Build Status Notification (Automated FYI)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "CI/CD — Build Notifications",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson"],
        "messages": [
            m("alexkumar", "FYI — nightly build #4582 completed successfully. All 847 tests passed. Deployment to staging was automatic.\n\nBuild: ✅ PASS\nTests: 847/847 ✅\nCoverage: 94.2%\nStaging: Deployed ✅",
              notes="Build notification — automated FYI"),
            m("priyasharma", "Clean build! The test count went up by 12 from my new API tests. 👍",
              notes="Observation"),
            m("jameswilson", "Staging looks good on the infrastructure side too. Load balancer health checks all passing.",
              notes="Status confirmation"),
        ],
    },

]
