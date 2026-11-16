"""
Descriptive and clinical-support content for each Enneagram type.

Written independently for this tool, synthesizing widely-published, public-domain
Enneagram theory (core fears/desires, centers, wings, arrows, levels of health).
Framed for use by a therapist alongside a client, not as a stand-alone diagnosis.
"""

TYPE_PROFILES = {
    1: {
        "name": "The Reformer",
        "alt_names": "The Perfectionist, The Rational Idealist",
        "core_fear": "Being bad, corrupt, defective, or wrong.",
        "core_desire": "To be good, to have integrity, to be balanced.",
        "core_motivation": "Striving to live up to an inner ideal of 'rightness' and to improve themselves and the world.",
        "basic_pattern": (
            "Ones develop an acute inner critic early in life that constantly evaluates whether "
            "they (and the world around them) measure up to a standard of correctness. They "
            "channel a lot of energy into self-control, responsibility, and improvement, often at "
            "the cost of spontaneity and self-compassion."
        ),
        "healthy": "Wise, discerning, realistic, and morally courageous. Able to accept imperfection in themselves and others with grace.",
        "average": "Orderly, critical, perfectionistic. A strong inner judge drives rigid standards and frequent self-criticism.",
        "unhealthy": "Harshly condemning of self and others, rigid, self-righteous, and prone to obsessive or punitive thinking.",
        "stress_behaviors": "Becomes more rigid, irritable, and critical; may suppress anger until it leaks out sharply.",
        "growth_direction": "Moving toward Seven (growth): becomes more spontaneous, joyful, and able to let go of control.",
        "stress_direction": "Moving toward Four (stress): becomes moody, withdrawn, and prone to despair about not being 'good enough.'",
        "therapy_notes": (
            "Watch for perfectionism-driven anxiety, chronic self-criticism, and difficulty expressing anger directly "
            "(it often appears as irritability, tension, or passive resentment instead). Clients often respond well to "
            "work on self-compassion, body-based anger release, and loosening all-or-nothing standards."
        ),
        "questions_to_explore": [
            "What would it feel like to make a mistake and not judge yourself for it?",
            "Where in your body do you notice tension when you feel something is 'wrong'?",
            "Whose voice is your inner critic modeled on?",
            "What would 'good enough' look like, concretely, in this situation?",
        ],
    },
    2: {
        "name": "The Helper",
        "alt_names": "The Giver, The People-Pleaser",
        "core_fear": "Being unwanted, unworthy of love, or a burden to others.",
        "core_desire": "To feel loved and appreciated.",
        "core_motivation": "Seeking to earn love and connection by being indispensable to others.",
        "basic_pattern": (
            "Twos learn to focus outward, attuning closely to others' needs while suppressing their "
            "own. Self-worth becomes tied to being needed, which can create a cycle of giving "
            "followed by hidden resentment when their own needs go unacknowledged."
        ),
        "healthy": "Genuinely empathic, generous, and able to care for others while also caring for themselves.",
        "average": "Approval-seeking, overly accommodating, and prone to manipulating through giving (guilt, flattery) to secure love.",
        "unhealthy": "Self-sacrificing to the point of resentment, manipulative, or martyr-like; can collapse into helplessness.",
        "stress_behaviors": "Becomes more aggressive or demanding of appreciation, then may swing into exhaustion or helplessness.",
        "growth_direction": "Moving toward Four (growth): becomes more aware of and honest about their own needs and feelings.",
        "stress_direction": "Moving toward Eight (stress): becomes controlling, aggressive, or demanding when needs go unmet long enough.",
        "therapy_notes": (
            "Watch for difficulty naming personal needs, chronic over-giving, and indirect resentment. Helpful work "
            "includes boundary-setting practice, learning to tolerate others' disappointment, and identifying feelings "
            "and needs without first filtering them through 'what will this get me.'"
        ),
        "questions_to_explore": [
            "What do you need right now, independent of what anyone else needs?",
            "What happens inside you when you imagine saying 'no'?",
            "Who loved you before you had to earn it?",
            "What would it feel like to receive help instead of giving it?",
        ],
    },
    3: {
        "name": "The Achiever",
        "alt_names": "The Performer, The Succeeder",
        "core_fear": "Being worthless, or being seen as a failure.",
        "core_desire": "To feel valuable and worthwhile.",
        "core_motivation": "Striving to achieve, succeed, and be admired in order to prove their worth.",
        "basic_pattern": (
            "Threes learn that love and attention come through accomplishment and image, so they "
            "adapt themselves to whatever role brings success and approval - sometimes losing touch "
            "with their authentic feelings and desires in the process."
        ),
        "healthy": "Authentic, self-assured, and genuinely engaged, with success flowing from values rather than image.",
        "average": "Image-conscious, competitive, and workaholic; measures self-worth almost entirely by achievement.",
        "unhealthy": "Deceptive, exploitative of others for personal gain, and increasingly disconnected from genuine feeling.",
        "stress_behaviors": "Becomes more detached, overworked, and image-focused; may cut corners or disengage emotionally.",
        "growth_direction": "Moving toward Six (growth): becomes more loyal, cooperative, and genuinely committed to others.",
        "stress_direction": "Moving toward Nine (stress): becomes disengaged, numb, and procrastinating under prolonged pressure.",
        "therapy_notes": (
            "Watch for difficulty accessing genuine feeling underneath a polished presentation, workaholism, and "
            "fear of being 'found out' as ordinary or flawed. Helpful work includes slowing down enough to feel "
            "emotions as they arise, and separating self-worth from performance."
        ),
        "questions_to_explore": [
            "If no one were watching or evaluating you, what would you choose to do?",
            "What feeling might be underneath the drive to keep achieving?",
            "What would it mean about you if you failed at something publicly?",
            "Who are you when you're not performing?",
        ],
    },
    4: {
        "name": "The Individualist",
        "alt_names": "The Romantic, The Artist",
        "core_fear": "Having no identity, significance, or personal meaning.",
        "core_desire": "To find themselves and their unique significance.",
        "core_motivation": "Seeking to express a deeply felt, authentic identity and to be understood.",
        "basic_pattern": (
            "Fours develop a heightened sensitivity to feeling, often alongside a sense that something "
            "essential is missing in themselves compared to others. This creates a search for identity "
            "and meaning through intense emotional experience, aesthetics, and depth of feeling."
        ),
        "healthy": "Creative, emotionally honest, and deeply attuned to beauty and meaning, with a secure sense of identity.",
        "average": "Self-absorbed, melancholic, and prone to comparing themselves unfavorably to others, feeling 'different.'",
        "unhealthy": "Self-destructive, alienated, and overwhelmed by despair or shame; may push away support that could help.",
        "stress_behaviors": "Becomes more withdrawn, moody, and self-critical, dwelling on what's missing or wrong.",
        "growth_direction": "Moving toward One (growth): becomes more disciplined, objective, and able to act despite feelings.",
        "stress_direction": "Moving toward Two (stress): becomes clingy or over-involved in relationships to manage abandonment fears.",
        "therapy_notes": (
            "Watch for identity-based rumination, intense and shifting emotional states, and envy/comparison patterns. "
            "Helpful work includes grounding and emotional-regulation skills, building consistent routines, and "
            "distinguishing passing feelings from a stable sense of self."
        ),
        "questions_to_explore": [
            "What is actually happening right now, versus the story your feelings are telling you?",
            "What would it mean to feel secure in who you are, without needing to feel 'special'?",
            "What's one small, ordinary action you could take today, regardless of mood?",
            "Who sees and understands you well? What does that feel like?",
        ],
    },
    5: {
        "name": "The Investigator",
        "alt_names": "The Observer, The Thinker",
        "core_fear": "Being incapable, overwhelmed, or depleted by the demands of others.",
        "core_desire": "To be competent and self-sufficient.",
        "core_motivation": "Seeking to understand the world fully while conserving personal energy and resources.",
        "basic_pattern": (
            "Fives learn to retreat into the mind for safety, minimizing needs and withdrawing from "
            "emotional demands to conserve limited inner resources. Knowledge and privacy become a "
            "substitute for direct engagement with an often-overwhelming world."
        ),
        "healthy": "Perceptive, innovative, and genuinely engaged, sharing knowledge and presence generously.",
        "average": "Detached, private, and intellectualizing; keeps people at arm's length to avoid feeling drained.",
        "unhealthy": "Isolated, nihilistic, or eccentric to the point of total withdrawal from relationships and reality.",
        "stress_behaviors": "Withdraws further, becomes more detached or cynical, and avoids emotional contact.",
        "growth_direction": "Moving toward Eight (growth): becomes more decisive, engaged, and willing to act on what they know.",
        "stress_direction": "Moving toward Seven (stress): becomes scattered, impulsive, or escapist when overwhelmed.",
        "therapy_notes": (
            "Watch for intellectualizing feelings, minimizing needs, and withdrawing when overwhelmed. Helpful work "
            "includes building tolerance for emotional and relational presence, naming feelings in the body rather than "
            "just the mind, and practicing small acts of reaching out before fully withdrawing."
        ),
        "questions_to_explore": [
            "What are you feeling right now, in your body, not just thinking?",
            "What would it be like to ask for support before you're completely out of energy?",
            "What needs feel 'too much' to voice to other people?",
            "Where do you feel safe enough to be fully present with another person?",
        ],
    },
    6: {
        "name": "The Loyalist",
        "alt_names": "The Skeptic, The Guardian",
        "core_fear": "Being without support, guidance, or security.",
        "core_desire": "To feel secure and supported.",
        "core_motivation": "Scanning for danger and seeking reliable support, structure, or certainty.",
        "basic_pattern": (
            "Sixes develop a vigilant, questioning mind that anticipates problems and tests the "
            "trustworthiness of people and systems. This can show up as either seeking strong "
            "support (dependent/phobic style) or pushing against authority (counterphobic style)."
        ),
        "healthy": "Courageous, loyal, and a steady source of support for others, trusting their own judgment.",
        "average": "Anxious, suspicious, and prone to worst-case thinking; seeks reassurance or tests others' loyalty.",
        "unhealthy": "Paranoid, reactive, or paralyzed by anxiety; may lash out at perceived threats or authority.",
        "stress_behaviors": "Anxiety spikes, catastrophic thinking increases, and trust in self or others erodes.",
        "growth_direction": "Moving toward Nine (growth): becomes calmer, more trusting, and relaxed in their own judgment.",
        "stress_direction": "Moving toward Three (stress): becomes more image-focused, competitive, and detached from feelings under pressure.",
        "therapy_notes": (
            "Watch for anticipatory anxiety, difficulty trusting their own judgment, and either over-dependence on or "
            "rebellion against authority figures. Helpful work includes building a felt sense of inner authority, "
            "grounding/anxiety-management skills, and distinguishing real from imagined threats."
        ),
        "questions_to_explore": [
            "What does your own gut tell you, separate from what you fear others will think?",
            "What is the actual evidence for this worst-case scenario?",
            "Who or what have you learned you can reliably trust?",
            "What would it feel like to trust your own judgment just for today?",
        ],
    },
    7: {
        "name": "The Enthusiast",
        "alt_names": "The Epicure, The Generalist",
        "core_fear": "Being deprived, trapped, or stuck in pain.",
        "core_desire": "To be satisfied, content, and free.",
        "core_motivation": "Seeking stimulating experiences and future possibilities to avoid pain or limitation.",
        "basic_pattern": (
            "Sevens learn to reframe or escape discomfort quickly by moving toward novelty, options, "
            "and pleasurable experience. This keeps them upbeat and resourceful but can also create "
            "avoidance of necessary pain, grief, or follow-through."
        ),
        "healthy": "Joyful, spontaneous, and genuinely grateful, able to be fully present, including with difficulty.",
        "average": "Scattered, impulsive, and avoidant of pain; chases the 'next thing' rather than finishing the current one.",
        "unhealthy": "Escapist, impulsive to a self-destructive degree, and unable to tolerate any limitation or discomfort.",
        "stress_behaviors": "Becomes more scattered, impulsive, and escapist, piling on distractions to outrun difficult feelings.",
        "growth_direction": "Moving toward Five (growth): becomes more focused, reflective, and able to sit with depth.",
        "stress_direction": "Moving toward One (stress): becomes critical, rigid, and irritable when options feel cut off.",
        "therapy_notes": (
            "Watch for difficulty tolerating painful emotions, impulsivity, and a pattern of starting many things "
            "without finishing them. Helpful work includes building tolerance for sitting with uncomfortable "
            "feelings, slowing decision-making, and processing unresolved grief or loss."
        ),
        "questions_to_explore": [
            "What feeling are you moving away from right now?",
            "What would happen if you let yourself feel this fully for just a minute?",
            "What's one thing you'd be willing to finish before starting something new?",
            "What does 'enough' feel like, rather than 'more'?",
        ],
    },
    8: {
        "name": "The Challenger",
        "alt_names": "The Protector, The Boss",
        "core_fear": "Being controlled, vulnerable, or harmed by others.",
        "core_desire": "To protect themselves and determine their own course in life.",
        "core_motivation": "Asserting control and strength to avoid being dominated or betrayed.",
        "basic_pattern": (
            "Eights learn early that vulnerability is dangerous, so they develop strength, directness, "
            "and control as protection. They move toward conflict rather than away from it, and often "
            "take charge to avoid depending on others' goodwill."
        ),
        "healthy": "Magnanimous, protective, and empowering of others, using strength in service of a larger good.",
        "average": "Domineering, confrontational, and resistant to vulnerability; leads through intimidation when stressed.",
        "unhealthy": "Ruthless, destructive, or vengeful, with a complete rejection of softness or dependency.",
        "stress_behaviors": "Becomes more controlling, confrontational, and less able to tolerate any sign of weakness.",
        "growth_direction": "Moving toward Two (growth): becomes more caring, open-hearted, and able to show tenderness.",
        "stress_direction": "Moving toward Five (stress): becomes withdrawn, secretive, and emotionally shut down under extreme stress.",
        "therapy_notes": (
            "Watch for discomfort with vulnerability, difficulty trusting others enough to depend on them, and anger "
            "as a primary or sole outward emotion. Helpful work includes building safety around softness, "
            "practicing asking for help, and separating control from genuine safety."
        ),
        "questions_to_explore": [
            "What would it feel like to let someone else see you as uncertain or hurt?",
            "Who, if anyone, have you let yourself truly depend on?",
            "What are you protecting by staying in control right now?",
            "What is underneath the anger in this moment?",
        ],
    },
    9: {
        "name": "The Peacemaker",
        "alt_names": "The Mediator, The Accommodator",
        "core_fear": "Loss of connection, separation, or conflict.",
        "core_desire": "To have inner stability, peace of mind, and wholeness.",
        "core_motivation": "Seeking harmony by merging with others' agendas and minimizing their own, to avoid conflict.",
        "basic_pattern": (
            "Nines learn to numb out their own preferences and anger to keep the peace, often merging "
            "with others' wishes. This creates a calm exterior, but can leave their own identity, "
            "priorities, and anger unexpressed and unresolved."
        ),
        "healthy": "Genuinely peaceful, inclusive, and self-possessed, bringing people together from a place of real inner stability.",
        "average": "Conflict-avoidant, indecisive, and prone to zoning out or procrastinating rather than asserting themselves.",
        "unhealthy": "Stubbornly disengaged, passive-aggressive, or completely dissociated from their own needs and life direction.",
        "stress_behaviors": "Becomes more withdrawn, stubborn, and passive, disengaging quietly rather than confronting problems.",
        "growth_direction": "Moving toward Three (growth): becomes more energized, self-directed, and willing to assert their priorities.",
        "stress_direction": "Moving toward Six (stress): becomes anxious, suspicious, and reactive under sustained pressure.",
        "therapy_notes": (
            "Watch for difficulty identifying personal preferences, conflict avoidance, and anger expressed indirectly "
            "(stonewalling, forgetting, procrastinating) rather than directly. Helpful work includes practicing "
            "naming preferences out loud, building tolerance for healthy conflict, and somatic anger awareness."
        ),
        "questions_to_explore": [
            "If your own wishes mattered as much as everyone else's, what would you choose here?",
            "What are you avoiding by staying comfortable right now?",
            "Where do you notice anger in your body, even if you don't 'feel angry'?",
            "What is one thing you want, independent of what would keep the peace?",
        ],
    },
}

LEVEL_BANDS = [
    (0, 40, "Likely Unhealthy Range",
     "Scores in this range suggest the client may currently be experiencing significant distress, "
     "rigid or compulsive patterns, and reduced capacity for self-reflection. This is a useful area "
     "to explore gently and supportively in session, not a fixed label."),
    (40, 70, "Likely Average Range",
     "Scores in this range suggest the client is functioning with the ordinary mix of coping "
     "strategies and blind spots most people have day-to-day - some flexibility, with recognizable "
     "defensive patterns under stress."),
    (70, 101, "Likely Healthy Range",
     "Scores in this range suggest the client currently has good access to self-awareness, "
     "flexibility, and resilience, with more freedom from their type's core fear than the average."),
]

CENTER_SUMMARY = {
    "Body (Gut) Center": "Relates primarily through instinct, control, and resistance; core emotional theme is anger/rage.",
    "Heart Center": "Relates primarily through image, identity, and relationship; core emotional theme is shame.",
    "Head Center": "Relates primarily through thinking, planning, and anticipation; core emotional theme is fear/anxiety.",
}

HARMONIC_TRIAD_DESC = {
    "Positive Outlook": "Copes with frustration by reframing it positively and moving attention away from "
                         "negativity - the trade-off can be minimizing real problems to stay upbeat.",
    "Competency": "Copes with frustration by setting feeling aside and solving the problem objectively - "
                  "the trade-off can be under-acknowledging emotion, their own or others'.",
    "Reactive": "Copes with frustration with visible emotional intensity and needs that intensity "
                "acknowledged before moving on - the trade-off can be escalation if it isn't.",
}

HORNEVIAN_GROUP_DESC = {
    "Assertive": "Pursues needs by moving toward/against resistance directly - taking up space, pushing "
                 "the situation to resolve on their terms.",
    "Compliant": "Pursues needs by moving toward an internalized standard, duty, or authority - working "
                 "within the system rather than pushing against it.",
    "Withdrawn": "Pursues needs by moving away internally - stepping back to process before (or instead "
                 "of) engaging the external situation directly.",
}

# Riso-Hudson's traditional type-specific Nine Levels of Development, grouped
# into the same three health bands this tool's own functioning scale uses -
# but note in FUNCTIONING_VS_LEVELS_NOTE below that the two are NOT the same
# measurement and one cannot be mathematically derived from the other.
RISO_HUDSON_LEVELS = [
    (1, "Healthy", "Level of Liberation"),
    (2, "Healthy", "Level of Psychological Capacity"),
    (3, "Healthy", "Level of Social Value"),
    (4, "Average", "Level of Imbalance / Social Role"),
    (5, "Average", "Level of Interpersonal Control"),
    (6, "Average", "Level of Overcompensation"),
    (7, "Unhealthy", "Level of Violation"),
    (8, "Unhealthy", "Level of Obsession and Compulsion"),
    (9, "Unhealthy", "Level of Pathological Destructiveness"),
]

FUNCTIONING_VS_LEVELS_NOTE = (
    "This tool's Functioning Score is a separate, general self-report wellbeing/capacity scale "
    "(15 original items, 0-100%), not the traditional Enneagram Levels of Development. Riso and "
    "Hudson's own Nine Levels are type-specific, clinically described in their books, and were never "
    "validated against a simple percentage self-report instrument. The three health bands this tool "
    "uses (Unhealthy/Average/Healthy) intentionally mirror the traditional levels' three-band grouping "
    "(Levels 7-9 / 4-6 / 1-3) for conceptual familiarity, but there is no defensible arithmetic "
    "conversion from this tool's percentage to a specific level 1-9. Report the percentage and band "
    "only - do not state or imply a specific traditional Level without separate clinical judgment."
)

FIX_DESCRIPTIONS = {
    "Body (Gut) Center": "Gut/Body Fix - the client's highest-scoring type among 8, 9, 1. Contributes the "
                          "instinctual/anger-center flavor of the tritype: how they assert, resist, or "
                          "control their environment.",
    "Heart Center": "Heart Fix - the client's highest-scoring type among 2, 3, 4. Contributes the "
                     "image/shame-center flavor: how they manage identity, image, and connection.",
    "Head Center": "Head Fix - the client's highest-scoring type among 5, 6, 7. Contributes the "
                    "thinking/fear-center flavor: how they plan, anticipate, and manage uncertainty.",
}

INSTINCT_POSITION_DESC = {
    "dominant": "Dominant - gets attention first and most automatically. Usually the instinct the client "
                "would describe as 'just how I operate' without much reflection.",
    "secondary": "Secondary - a supporting focus, engaged more consciously and more flexibly than the "
                 "dominant instinct, often used in service of it.",
    "blind_spot": "Blind Spot (least developed) - the most neglected instinctual focus. Not a weakness to "
                  "fix, but an area the client may under-resource or overlook, worth naming gently.",
}

ARROW_CLARIFICATION = (
    "Integration and disintegration describe behavior a person temporarily 'borrows' from another type "
    "under security/growth or stress, respectively - they are not evidence of a literal change in core "
    "type or a personality transformation. Core type remains constant; what shifts is which behaviors "
    "become more available under different conditions."
)
