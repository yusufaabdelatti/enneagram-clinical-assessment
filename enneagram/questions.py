"""
Original item bank for the Enneagram assessment.

All items are written independently for this tool - they are not copied from
any proprietary/commercial instrument (e.g. RHETI, iEQ9, Truity). They are
designed for use in a clinical/therapeutic context, not as a stand-alone
diagnostic tool.

Likert scale used for TYPE_ITEMS and INSTINCT_ITEMS:
    1 = Not at all like me
    2 = A little like me
    3 = Somewhat like me
    4 = Mostly like me
    5 = Very much like me

Likert scale used for FUNCTIONING_ITEMS:
    1 = Never / Not true
    2 = Rarely
    3 = Sometimes
    4 = Often
    5 = Almost always / Very true
"""

TYPE_NAMES = {
    1: "The Reformer",
    2: "The Helper",
    3: "The Achiever",
    4: "The Individualist",
    5: "The Investigator",
    6: "The Loyalist",
    7: "The Enthusiast",
    8: "The Challenger",
    9: "The Peacemaker",
}

# Adjacent wings for each type
WINGS = {
    1: (9, 2),
    2: (1, 3),
    3: (2, 4),
    4: (3, 5),
    5: (4, 6),
    6: (5, 7),
    7: (6, 8),
    8: (7, 9),
    9: (8, 1),
}

# Centers / triads
CENTERS = {
    "Body (Gut) Center": [8, 9, 1],
    "Heart Center": [2, 3, 4],
    "Head Center": [5, 6, 7],
}

# Growth (integration) / Stress (disintegration) arrows, per classic Enneagram theory
INTEGRATION_ARROW = {1: 7, 7: 5, 5: 8, 8: 2, 2: 4, 4: 1, 3: 6, 6: 9, 9: 3}
DISINTEGRATION_ARROW = {1: 4, 4: 2, 2: 8, 8: 5, 5: 7, 7: 1, 3: 9, 9: 6, 6: 3}

# Harmonic triads (Riso-Hudson) - how a type characteristically copes with
# frustration/disappointment, independent of its Center of Intelligence.
HARMONIC_TRIADS = {
    "Positive Outlook": [2, 7, 9],
    "Competency": [1, 3, 5],
    "Reactive": [4, 6, 8],
}

# Hornevian groups (named for Karen Horney's "moving toward/against/away"
# framework; Horney did not map this to the Enneagram herself - later
# Enneagram teachers, principally Riso and Hudson, found the alignment).
# Describes how a type characteristically pursues its needs relative to others.
HORNEVIAN_GROUPS = {
    "Assertive": [3, 7, 8],
    "Compliant": [1, 2, 6],
    "Withdrawn": [4, 5, 9],
}


def harmonic_triad_for(type_num):
    for name, members in HARMONIC_TRIADS.items():
        if type_num in members:
            return name
    return None


def hornevian_group_for(type_num):
    for name, members in HORNEVIAN_GROUPS.items():
        if type_num in members:
            return name
    return None

# ---------------------------------------------------------------------------
# Core 108-item type scale (12 items x 9 types)
# ---------------------------------------------------------------------------
TYPE_ITEMS = [
    # Type 1 - The Reformer
    (1, "I hold myself to very high standards and feel uneasy when I fall short of them."),
    (1, "I notice errors or things that are 'not quite right' before most people do."),
    (1, "I feel a strong inner voice telling me what is the correct or proper way to do things."),
    (1, "I work hard to be fair, responsible, and honest in everything I do."),
    (1, "I can be harshly critical of myself when I make mistakes."),
    (1, "I get frustrated when other people don't put in the same effort or care that I do."),
    (1, "I believe there is usually a right way and a wrong way to do things."),
    (1, "I feel a responsibility to improve things around me, even when no one asked me to."),
    (1, "I suppress my anger because I don't think it's acceptable to express it."),
    (1, "I plan and organize things carefully rather than leaving them to chance."),
    (1, "I feel guilty when I relax or indulge myself instead of being productive."),
    (1, "People have told me I can be a perfectionist or overly strict."),

    # Type 2 - The Helper
    (2, "I feel most fulfilled when I'm taking care of the people close to me."),
    (2, "I often put other people's needs ahead of my own without being asked."),
    (2, "I find it hard to ask directly for help, even when I need it."),
    (2, "I pay close attention to what other people need, sometimes before they realize it themselves."),
    (2, "I feel hurt or taken for granted when my efforts for others go unnoticed."),
    (2, "I like to be seen as warm, generous, and indispensable to the people I love."),
    (2, "I struggle to say no to requests from people I care about."),
    (2, "I shape how I act depending on who I'm with, to make sure they feel cared for."),
    (2, "I feel uncomfortable or guilty when I focus on my own needs."),
    (2, "I tend to give people compliments, favors, or gifts to build closeness."),
    (2, "I sometimes feel resentful underneath, even while I keep giving to others."),
    (2, "I measure my own worth by how much I'm needed by others."),

    # Type 3 - The Achiever
    (3, "I feel driven to succeed and to be seen as competent or accomplished."),
    (3, "I naturally focus on efficiency and getting results."),
    (3, "I adapt my image depending on what will help me succeed in a given situation."),
    (3, "I feel uncomfortable with failure or being seen as a loser."),
    (3, "I set ambitious goals for myself and feel restless until I reach them."),
    (3, "I find it hard to slow down, even when I'm exhausted."),
    (3, "I care a lot about how others perceive my achievements and status."),
    (3, "I sometimes lose touch with my own feelings while chasing a goal."),
    (3, "I present a polished, confident version of myself, even if I feel differently inside."),
    (3, "I compare my accomplishments with other people's."),
    (3, "I feel my value is tied to being productive or successful."),
    (3, "I move quickly from one task or goal to the next without pausing to reflect."),

    # Type 4 - The Individualist
    (4, "I feel deeply, and my emotions can shift intensely from one moment to the next."),
    (4, "I often feel different from other people, like something sets me apart."),
    (4, "I'm drawn to beauty, meaning, and authenticity in how I express myself."),
    (4, "I sometimes feel a persistent sense of longing or that something important is missing."),
    (4, "I can become envious when I see qualities or experiences in others that I feel I lack."),
    (4, "I value being seen and understood for who I truly am, not for how I appear."),
    (4, "I find ordinary routines unsatisfying compared to moments of deep feeling or meaning."),
    (4, "I can be quite self-critical, especially about not living up to my own ideals."),
    (4, "My mood strongly affects how I relate to the people and world around me."),
    (4, "I'm drawn to creative outlets like art, writing, or music to express my inner world."),
    (4, "I can withdraw into my own feelings when life feels overwhelming or ordinary."),
    (4, "I feel most alive when an experience feels emotionally significant or meaningful."),

    # Type 5 - The Investigator
    (5, "I need a lot of private time to think, recharge, and process on my own."),
    (5, "I prefer observing and understanding a situation before participating in it."),
    (5, "I feel uncomfortable when people make emotional demands on me without warning."),
    (5, "I enjoy gathering knowledge and becoming an expert in subjects that interest me."),
    (5, "I'm careful about how much of my energy, time, or resources I share with others."),
    (5, "I tend to analyze my feelings mentally rather than express them in the moment."),
    (5, "I value having my own space, both physically and emotionally."),
    (5, "I often feel like I have limited energy and need to ration it carefully."),
    (5, "I prefer to think things through fully before I speak or act."),
    (5, "I can seem detached or reserved even when I care deeply."),
    (5, "I would rather read, research, or reflect than engage in small talk."),
    (5, "I feel safest when I have enough information and don't feel caught off guard."),

    # Type 6 - The Loyalist
    (6, "I tend to imagine what could go wrong before it happens."),
    (6, "I value loyalty and look for people or systems I can trust."),
    (6, "I often look to double-check decisions, even ones I've already made."),
    (6, "I can be suspicious of other people's motives until they've earned my trust."),
    (6, "I feel reassured when I know what to expect and anxious when I don't."),
    (6, "I prepare for worst-case scenarios so I won't be caught off guard."),
    (6, "I sometimes swing between seeking support and pushing back against authority."),
    (6, "I take commitments and responsibilities very seriously."),
    (6, "I look for reassurance from others when I'm uncertain about a decision."),
    (6, "I question or test the intentions of people in positions of authority."),
    (6, "I feel more confident when I have backup, allies, or a plan for problems."),
    (6, "My mind tends to run through multiple possibilities, including the negative ones."),

    # Type 7 - The Enthusiast
    (7, "I'm drawn to new experiences, ideas, and possibilities."),
    (7, "I have a hard time sitting with painful or uncomfortable feelings."),
    (7, "I keep my options open and dislike feeling boxed in or restricted."),
    (7, "I naturally look for the upside or silver lining in difficult situations."),
    (7, "I get bored or restless when things stay the same for too long."),
    (7, "I tend to jump quickly from one idea, plan, or project to another."),
    (7, "I use humor, activity, or future plans to lift my mood when I feel down."),
    (7, "I have a wide range of interests and find it hard to choose just one."),
    (7, "I feel most alive when I'm doing something fun, stimulating, or spontaneous."),
    (7, "I avoid conversations or situations that feel heavy or draining."),
    (7, "I find it difficult to finish things once the initial excitement fades."),
    (7, "I would rather stay upbeat than dwell on limitations or losses."),

    # Type 8 - The Challenger
    (8, "I speak up directly and don't shy away from confrontation when it's needed."),
    (8, "I feel a strong need to be in control of my own life and decisions."),
    (8, "I have a hard time showing vulnerability, even to people I trust."),
    (8, "I naturally take charge in group situations."),
    (8, "I respect people who are strong and direct, and lose respect for those who aren't."),
    (8, "I feel intensely protective of people I consider 'mine' to look after."),
    (8, "I push back hard against anyone who tries to control or manipulate me."),
    (8, "I can come across as more intense or forceful than I intend to."),
    (8, "I trust my own instincts and decisions more than relying on others."),
    (8, "I have a lot of energy and like to use it to make things happen."),
    (8, "I find it hard to tolerate weakness, in myself or others."),
    (8, "I prefer dealing with conflict head-on rather than letting it simmer."),

    # Type 9 - The Peacemaker
    (9, "I go out of my way to avoid conflict and keep the peace."),
    (9, "I find it easier to see other people's points of view than to know my own."),
    (9, "I tend to put off decisions or difficult tasks for as long as I can."),
    (9, "I feel most comfortable when things around me are calm and harmonious."),
    (9, "I sometimes merge with other people's wishes instead of asserting my own."),
    (9, "I can lose track of time doing comfortable, familiar, or distracting activities."),
    (9, "I have a hard time identifying what I personally want."),
    (9, "I stay easygoing on the surface, even when I feel strongly underneath."),
    (9, "I prefer to let things unfold rather than push to make something happen."),
    (9, "I withdraw or become stubborn quietly rather than argue outright."),
    (9, "I can be a calming, steady presence for people around me in stressful moments."),
    (9, "I avoid expressing my anger directly, and it comes out in indirect ways instead."),
]

# ---------------------------------------------------------------------------
# Instinctual variant scale (9 items x 3 instincts = 27 items)
# ---------------------------------------------------------------------------
INSTINCT_NAMES = {
    "sp": "Self-Preservation",
    "so": "Social",
    "sx": "Sexual / One-to-One",
}

INSTINCT_ITEMS = [
    ("sp", "I pay close attention to my physical comfort, health, routines, and security."),
    ("sp", "I think a lot about practical matters like money, safety, home, and resources."),
    ("sp", "I feel unsettled when my basic needs (sleep, food, environment) are disrupted."),
    ("sp", "I'm drawn to building a stable, comfortable personal foundation before anything else."),
    ("sp", "I notice and manage small physical details in my environment without much effort."),
    ("sp", "I prioritize self-care and maintaining my energy and wellbeing."),
    ("sp", "I'm cautious about unnecessary risks that could threaten my stability."),
    ("sp", "I like having a reliable routine that keeps my daily life running smoothly."),
    ("sp", "I feel most secure when my personal resources (time, money, energy) are well managed."),
    ("so", "I'm very aware of group dynamics, status, and how I fit into a community."),
    ("so", "I care about belonging to groups, causes, or communities that matter to me."),
    ("so", "I think about my responsibilities and role within the larger group or society."),
    ("so", "I notice who has influence, respect, or standing within a group."),
    ("so", "I feel energized by being involved in shared projects, teams, or causes."),
    ("so", "I pay attention to social rules, etiquette, and how groups expect people to behave."),
    ("so", "I want to contribute something meaningful to the wider community, not just myself."),
    ("so", "I'm concerned with being valued, respected, or recognized within my social circle."),
    ("so", "I find myself comparing my social position or participation with others around me."),
    ("sx", "I'm drawn to intense, one-on-one connections more than group interaction."),
    ("sx", "I look for chemistry, intensity, or a spark in my closest relationships."),
    ("sx", "I can become consumed or preoccupied by a person or attraction that interests me."),
    ("sx", "I feel most alive during an intense, charged encounter with another person."),
    ("sx", "I'm drawn to novelty, intensity, and crossing thresholds rather than staying safe."),
    ("sx", "I focus my energy intensely on one relationship or pursuit at a time."),
    ("sx", "I crave deep merging or a sense of being completely seen by one other person."),
    ("sx", "I'm sensitive to subtle shifts of attraction, desire, or energy between myself and others."),
    ("sx", "I prefer depth and intensity in a few key relationships over many casual ones."),
]

# ---------------------------------------------------------------------------
# General functioning / integration-level scale (15 items)
# Used to give an approximate indicator of current level of psychological
# functioning (healthy / average / unhealthy ranges), inspired by Riso-Hudson's
# publicly described "Levels of Development" concept but written independently.
# This is NOT a clinical diagnostic tool - framed to the therapist as a
# conversation starter only.
# ---------------------------------------------------------------------------
FUNCTIONING_ITEMS = [
    "I feel generally free to be myself, even under stress.",
    "I can observe my own patterns and reactions with some distance, rather than being consumed by them.",
    "My relationships feel mutual and flexible rather than rigid or compulsive.",
    "I can tolerate uncomfortable emotions without immediately needing to escape or fix them.",
    "I feel like I have real choice in how I respond to situations, rather than feeling driven by habit.",
    "I recover relatively well after stress, conflict, or disappointment.",
    "I can hold a balanced view of myself - seeing both my strengths and my flaws without extremes.",
    "I can adapt my usual patterns when a situation calls for something different.",
    "I feel a reasonable sense of inner security that doesn't depend entirely on outside circumstances.",
    "When I notice an unhealthy pattern in myself, I'm able to pause and shift course.",
    "I generally feel more energized and resourced than depleted and defensive.",
    "My coping strategies tend to help me rather than create new problems.",
    "I'm able to stay connected to others even when I'm under pressure.",
    "I don't feel trapped or compulsively driven by my core fears most of the time.",
    "Overall, I feel like I'm growing and functioning well in my life right now.",
]
