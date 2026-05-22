from datetime import datetime

from .auth import hash_password
from .game_descriptions import PAGE_DESCRIPTION_OVERRIDES
from .models import ActivityLog, Game, Genre, Rating, Review, User


GENRE_NAMES = [
    "Action",
    "Adventure",
    "Classic",
    "Competitive",
    "Co-op",
    "Crime",
    "Horror",
    "MOBA",
    "Multiplayer",
    "Open World",
    "Puzzle",
    "RPG",
    "Racing",
    "Shooter",
    "Simulation",
    "Stealth",
    "Story Rich",
    "Strategy",
    "Survival",
    "Superhero",
]


def requirements(cpu="Intel Core i5 / AMD Ryzen 5", ram="8 GB", gpu="NVIDIA GTX 970 / AMD RX 570", storage="30 GB"):
    return (
        "OS: Windows 10/11 64-bit\n"
        f"CPU: {cpu}\n"
        f"RAM: {ram}\n"
        f"GPU: {gpu}\n"
        f"Storage: {storage}"
    )


GAME_CATALOG = [
    ("Alan Wake", "Alan_Wake.jpg", ["Horror", "Story Rich", "Action"]),
    ("Alien: Isolation", "Alien_Isolation.jpg", ["Horror", "Survival", "Story Rich"]),
    ("Amnesia: A Machine for Pigs", "Amnesia_A_Machine_For_Pigs.jpg", ["Horror", "Adventure", "Story Rich"]),
    ("Amnesia: Rebirth", "Amnesia_Rebirth.jpg", ["Horror", "Adventure", "Story Rich"]),
    ("Amnesia: The Bunker", "Amnesia_The_Bunker.jpg", ["Horror", "Survival", "Stealth"]),
    ("Amnesia: The Dark Descent", "Amnesia_The_Dark_Descent.jpg", ["Horror", "Survival", "Classic"]),
    ("Assassin's Creed Unity", "Assasin_s_Creed_Unity.jpg", ["Action", "Adventure", "Open World", "Stealth"]),
    ("Atomic Heart", "Atomic_Heart.jpg", ["Shooter", "Action", "Story Rich"]),
    ("Baldur's Gate 3", "Baldurs_Gate_3.jpg", ["RPG", "Adventure", "Story Rich"]),
    ("Batman: Arkham Asylum", "Batman_Arkham_Asylum.jpg", ["Action", "Adventure", "Superhero"]),
    ("Batman: Arkham City", "Batman_Arkham_City.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Batman: Arkham Knight", "Batman_Arkham_Knight.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Batman: Arkham Origins", "Batman_Arkham_Origins.jpg", ["Action", "Adventure", "Superhero"]),
    ("Battlefield 1 Revolution", "Battlefield_1_Revolution.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("Battlefield 4", "Battlefield_4.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("Battlefield V", "Battlefield_V.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("BioShock 2", "Bioshock_2.jpg", ["Shooter", "Story Rich", "Action"]),
    ("Black Myth: Wukong", "Black_Myth_Wukong.jpg", ["Action", "RPG", "Adventure"]),
    ("Buckshot Roulette", "Buckshot_Roulette.jpg", ["Horror", "Strategy"]),
    ("Chained Together", "Chained_together.jpg", ["Co-op", "Adventure", "Puzzle"]),
    ("Civilization VI", "Civilization_6.jpg", ["Strategy", "Simulation", "Multiplayer"]),
    ("Counter-Strike 2", "Counter_Strike_2.jpg", ["Shooter", "Competitive", "Action"]),
    ("Cyberpunk 2077", "Cyberpunk_2077.jpg", ["RPG", "Open World", "Story Rich"]),
    ("Darkwood", "Darkwood.jpg", ["Horror", "Survival", "Story Rich"]),
    ("Detroit: Become Human", "Detroit_Become_Human.jpg", ["Adventure", "Story Rich"]),
    ("Dota 2", "Dota_2.jpg", ["MOBA", "Competitive", "Strategy"]),
    ("Elden Ring", "Elden_Ring.jpg", ["RPG", "Action", "Open World"]),
    ("Factorio", "Factorio.jpg", ["Strategy", "Simulation"]),
    ("Far Cry 3", "Far_Cry_3.jpg", ["Shooter", "Action", "Open World"]),
    ("Fallout 4", "Fallout_4.jpg", ["RPG", "Shooter", "Open World"]),
    ("Fallout: New Vegas", "Fallout_New_Vegas.jpg", ["RPG", "Shooter", "Open World", "Story Rich"]),
    ("Fears to Fathom: Carson House", "Fears_to_Fathom_Carson_House.jpg", ["Horror", "Story Rich"]),
    ("Fears to Fathom: Home Alone", "Fears_to_Fathom_Home_Alone.jpg", ["Horror", "Story Rich"]),
    ("Fears to Fathom: Ironbark Lookout", "Fears_to_Fathom_Ironbark_Lookout.jpg", ["Horror", "Story Rich"]),
    ("Fears to Fathom: Norwood Hitchhike", "Fears_to_Fathom_Norwood_Hitchhike.jpg", ["Horror", "Story Rich"]),
    ("Fears to Fathom: Woodbury Getaway", "Fears_to_Fathom_Woodbury_Getaway.jpg", ["Horror", "Story Rich"]),
    ("Firewatch", "Firewatch.jpg", ["Adventure", "Story Rich"]),
    ("FlatOut 2", "Flatout_2.jpg", ["Racing", "Action", "Classic"]),
    ("Grand Theft Auto III - Definitive Edition", "GTA_3_Definitive_Edition.jpg", ["Crime", "Action", "Open World"]),
    ("Grand Theft Auto IV", "GTA_4.jpg", ["Crime", "Action", "Open World", "Story Rich"]),
    ("Grand Theft Auto: San Andreas - Definitive Edition", "GTA_San_Andreas_Definitive_Edition.jpg", ["Crime", "Action", "Open World"]),
    ("Grand Theft Auto V", "GTA_V.jpg", ["Crime", "Action", "Open World"]),
    ("Grand Theft Auto: Vice City - Definitive Edition", "GTA_Vice_City_Definitive_Edition.jpg", ["Crime", "Action", "Open World"]),
    ("Hades", "Hades.jpg", ["Action", "RPG"]),
    ("Helldivers 2", "Helldivers_2.jpg", ["Shooter", "Co-op", "Action"]),
    ("Hitman 2: Silent Assassin", "Hitman_2_Silent_Assassin.jpg", ["Stealth", "Action", "Puzzle"]),
    ("Hitman: Absolution", "Hitman_Absolution.jpg", ["Stealth", "Action"]),
    ("Hitman: Blood Money", "Hitman_Blood_Money.jpg", ["Stealth", "Action", "Puzzle"]),
    ("Hitman: Codename 47", "Hitman_Codename_47.jpg", ["Stealth", "Action", "Classic"]),
    ("Hitman: Contracts", "Hitman_Contracts.jpg", ["Stealth", "Action"]),
    ("Hitman World of Assassination", "Hitman_World_Of_Assassination.jpg", ["Stealth", "Action", "Puzzle"]),
    ("Hogwarts Legacy", "Hogwarts_Legacy.jpg", ["RPG", "Adventure", "Open World"]),
    ("Just Cause", "Just_Cause.jpg", ["Action", "Open World", "Adventure"]),
    ("Mafia II", "Mafia_2.jpg", ["Crime", "Action", "Story Rich"]),
    ("Mafia III", "Mafia_3.jpg", ["Crime", "Action", "Open World"]),
    ("Manhunt", "Manhunt.jpg", ["Horror", "Stealth", "Action"]),
    ("Max Payne", "Max_Payne.jpg", ["Action", "Shooter", "Classic"]),
    ("Max Payne 2", "Max_Payne_2.jpg", ["Action", "Shooter", "Story Rich"]),
    ("Max Payne 3", "Max_Payne_3.jpg", ["Action", "Shooter", "Story Rich"]),
    ("Medal of Honor", "Medal_of_Honor.jpg", ["Shooter", "Action", "Classic"]),
    ("Microsoft Flight Simulator", "Microsoft_Flight_Simulator.jpg", ["Simulation", "Adventure"]),
    ("Mimic Search", "Mimic_Search.jpg", ["Horror", "Puzzle"]),
    ("Missing Hiker", "Missing_Hiker.jpg", ["Horror", "Adventure"]),
    ("Mouthwashing", "Mouthwashing.jpg", ["Horror", "Story Rich"]),
    ("Outlast", "Outlast.jpg", ["Horror", "Survival", "Stealth"]),
    ("Penumbra: Black Plague", "Penumbra_Black_Plague.jpg", ["Horror", "Puzzle", "Story Rich"]),
    ("Penumbra: Overture", "Penumbra_Overture.jpg", ["Horror", "Puzzle", "Story Rich"]),
    ("Phasmophobia", "Phasmophobia.jpg", ["Horror", "Co-op", "Survival"]),
    ("Portal", "Portal.jpg", ["Puzzle", "Story Rich", "Classic"]),
    ("Portal 2", "Portal_2.jpg", ["Puzzle", "Co-op", "Story Rich"]),
    ("Prey", "Prey.jpg", ["Shooter", "RPG", "Story Rich"]),
    ("Red Dead Redemption", "Red_Dead_Redemption.jpg", ["Action", "Open World", "Story Rich"]),
    ("Red Dead Redemption 2", "Red_Dead_Redemption_2.jpg", ["Action", "Open World", "Story Rich"]),
    ("Resident Evil 0", "Resident_Evil_0.jpg", ["Horror", "Survival", "Classic"]),
    ("Resident Evil 2", "Resident_Evil_2.jpg", ["Horror", "Survival", "Action"]),
    ("Resident Evil 4", "Resident_Evil_4.jpg", ["Horror", "Action", "Survival"]),
    ("Rise of the Tomb Raider", "Rise_of_the_Tomb_Raider.jpg", ["Action", "Adventure", "Puzzle"]),
    ("Rust", "Rust.jpg", ["Survival", "Open World", "Co-op"]),
    ("Silent Hill 2", "Silent_Hill_2.jpg", ["Horror", "Story Rich"]),
    ("Silent Hill f", "Silent_Hill_f.jpg", ["Horror", "Story Rich"]),
    ("SOMA", "SOMA.jpg", ["Horror", "Story Rich"]),
    ("Spider-Man Remastered", "Spider_man_Remastered.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Stardew Valley", "Stardew_Valley.jpg", ["Simulation", "Adventure", "Co-op"]),
    ("Subnautica", "Subnautica.jpg", ["Survival", "Adventure", "Open World"]),
    ("Terraria", "Terraria.jpg", ["Adventure", "Survival", "Co-op"]),
    ("That Which Gave Chase", "That_Which_Gave_Chase.jpg", ["Horror", "Adventure"]),
    ("The Last of Us Part I", "The_Last_of_Us_Part_I.jpg", ["Action", "Adventure", "Story Rich"]),
    ("The Witcher 3: Wild Hunt", "The_Witcher_3_Wild_Hunt.jpg", ["RPG", "Open World", "Story Rich"]),
    ("Tomb Raider", "Tomb_Raider.jpg", ["Action", "Adventure", "Puzzle"]),
    ("Tomb Raider: Anniversary", "Tomb_Raider_Anniversary.jpg", ["Action", "Adventure", "Puzzle"]),
    ("Tomb Raider: Legend", "Tomb_Raider_Legend.jpg", ["Action", "Adventure", "Puzzle"]),
    ("Tomb Raider: Underworld", "Tomb_Raider_Underworld.jpg", ["Action", "Adventure", "Puzzle"]),
]


SPECIAL_TEXT = {
    "Hogwarts Legacy": (
        "A magical open-world RPG full of spells, secrets, and chaotic student energy.",
        "Explore Hogwarts, Hogsmeade, and the Forbidden Forest while learning spells, brewing potions, and dealing with ancient mysteries. It is a generous adventure for players who want magic, exploration, and a lot of collectible distractions.",
        requirements(storage="85 GB"),
    ),
    "Factorio": (
        "Build the factory, defend the factory, become the factory.",
        "Mine ore, automate production chains, and slowly turn a quiet planet into an industrial machine. It starts with one conveyor belt and somehow ends with you optimizing copper throughput at 3 AM.",
        requirements(cpu="Intel Core i3 / AMD Ryzen 3", ram="8 GB", gpu="OpenGL 3.3 compatible GPU", storage="4 GB"),
    ),
    "Portal 2": (
        "A brilliant puzzle comedy about portals, test chambers, and suspicious robots.",
        "Solve spatial puzzles with a portal gun, listen to some of the sharpest dialogue in games, and try not to trust every friendly voice coming from the ceiling.",
        requirements(cpu="Intel Core i3 / AMD Ryzen 3", ram="4 GB", gpu="NVIDIA GTX 650 / AMD HD 7750", storage="8 GB"),
    ),
    "Firewatch": (
        "A quiet first-person mystery with beautiful views and tense radio conversations.",
        "Spend a summer in the Wyoming wilderness as a fire lookout and slowly uncover what is happening around you. It is calm, emotional, and easy to finish in one memorable evening.",
        requirements(cpu="Intel Core i3 / AMD Ryzen 3", ram="6 GB", gpu="NVIDIA GTX 650 / AMD HD 7750", storage="4 GB"),
    ),
    "Counter-Strike 2": (
        "A competitive tactical shooter where every corner has a lesson waiting.",
        "Team up, manage economy, learn maps, and discover that your crosshair placement becomes a personality trait after a few matches.",
        requirements(ram="8 GB", gpu="NVIDIA GTX 1060 / AMD RX 580", storage="85 GB"),
    ),
    "Baldur's Gate 3": (
        "A cinematic party RPG packed with choices, dice rolls, and memorable chaos.",
        "Travel through a reactive fantasy world, build a party full of very strong personalities, and solve problems with strategy, dialogue, or complete nonsense if the dice allow it.",
        requirements(cpu="Intel Core i5-4690 / AMD FX 8350", ram="16 GB", gpu="NVIDIA GTX 970 / AMD RX 480", storage="150 GB"),
    ),
    "Cyberpunk 2077": (
        "A stylish open-world RPG about ambition, chrome, and dangerous side jobs.",
        "Night City is loud, neon, and full of stories. It is the kind of game where you enter for the main quest and stay because every district keeps offering a different mood.",
        requirements(cpu="Intel Core i7-6700 / AMD Ryzen 5 1600", ram="12 GB", gpu="NVIDIA RTX 2060 / AMD RX 5700 XT", storage="70 GB"),
    ),
    "Elden Ring": (
        "A vast action RPG that rewards patience, curiosity, and controlled panic.",
        "Ride across an enormous fantasy world, challenge bosses that absolutely mean business, and slowly build the confidence required to walk into places that previously erased you in seconds.",
        requirements(cpu="Intel Core i7-8700K / AMD Ryzen 5 3600X", ram="16 GB", gpu="NVIDIA GTX 1070 / AMD RX Vega 56", storage="60 GB"),
    ),
    "Hades": (
        "A fast action roguelike where every failed run somehow makes you want one more attempt.",
        "Battle out of the Underworld, talk to a remarkably patient cast of gods and ghosts, and enjoy the rare game where repetition feels like momentum instead of grind.",
        requirements(cpu="Intel Core i5 / AMD Ryzen 5", ram="8 GB", gpu="NVIDIA GTX 950 / AMD RX 560", storage="15 GB"),
    ),
    "Red Dead Redemption 2": (
        "A cinematic open-world western with huge landscapes and even bigger attention to detail.",
        "Ride through a beautiful and fading frontier, get distracted by strangers, weather, card games, and long scenic trips, then remember there is still a dramatic main story waiting for you.",
        requirements(cpu="Intel Core i7-4770K / AMD Ryzen 5 1500X", ram="12 GB", gpu="NVIDIA GTX 1060 6GB / AMD RX 480 4GB", storage="150 GB"),
    ),
    "Stardew Valley": (
        "A cozy farming and life sim that quietly steals entire weekends.",
        "Grow crops, improve your farm, meet the local townspeople, and discover that a game can feel both productive and relaxing at the same time.",
        requirements(cpu="Intel Core i3 / AMD Ryzen 3", ram="4 GB", gpu="OpenGL 3.3 compatible GPU", storage="1 GB"),
    ),
    "Subnautica": (
        "An underwater survival adventure with beautiful views and very alarming sounds.",
        "Dive deeper into an alien ocean, craft better equipment, and keep convincing yourself that the next dark trench probably contains useful materials and not terrible news.",
        requirements(cpu="Intel Core i5 / AMD Ryzen 5", ram="8 GB", gpu="NVIDIA GTX 960 / AMD R9 280", storage="20 GB"),
    ),
    "The Witcher 3: Wild Hunt": (
        "A story-rich open-world RPG with strong quests, monsters, and difficult moral choices.",
        "Hunt creatures, follow political drama, and keep getting pulled into side quests that are often better written than entire games elsewhere.",
        requirements(cpu="Intel Core i5-2500K / AMD Phenom II X4 940", ram="8 GB", gpu="NVIDIA GTX 770 / AMD R9 290", storage="60 GB"),
    ),
}


DEMO_USERS = [
    {"username": "DemoPlayer", "email": "demo@playnext.com", "password": "demo12345", "genres": ["RPG", "Story Rich", "Open World"]},
    {"username": "VoldemortFan69", "email": "voldemortfan69@playnext.local", "password": "demo12345", "genres": ["RPG", "Adventure"]},
    {"username": "NapoleonTinyButMighty", "email": "napoleon@playnext.local", "password": "demo12345", "genres": ["Strategy", "Action"]},
    {"username": "GravityGuruNewton", "email": "newton@playnext.local", "password": "demo12345", "genres": ["Puzzle", "Story Rich"]},
    {"username": "LoreLynx", "email": "lorelynx@playnext.local", "password": "demo12345", "genres": ["RPG", "Story Rich"]},
    {"username": "MapMarkerMia", "email": "mia@playnext.local", "password": "demo12345", "genres": ["Open World", "Adventure"]},
    {"username": "LateShiftLeo", "email": "leo@playnext.local", "password": "demo12345", "genres": ["Action", "Shooter"]},
    {"username": "StorySnack", "email": "snack@playnext.local", "password": "demo12345", "genres": ["Story Rich", "Adventure"]},
    {"username": "WeekendRanger", "email": "ranger@playnext.local", "password": "demo12345", "genres": ["Action", "Open World"]},
    {"username": "NightShiftNina", "email": "nina@playnext.local", "password": "demo12345", "genres": ["Horror", "Story Rich"]},
    {"username": "CouchCoopMax", "email": "max@playnext.local", "password": "demo12345", "genres": ["Co-op", "Adventure"]},
    {"username": "TacticalTanya", "email": "tanya@playnext.local", "password": "demo12345", "genres": ["Strategy", "Simulation"]},
    {"username": "RacingToast", "email": "toast@playnext.local", "password": "demo12345", "genres": ["Racing", "Action"]},
    {"username": "PixelArchivist", "email": "archivist@playnext.local", "password": "demo12345", "genres": ["Classic", "Story Rich"]},
    {"username": "SeaLevelSue", "email": "sue@playnext.local", "password": "demo12345", "genres": ["Survival", "Adventure"]},
    {"username": "CozyNomad", "email": "nomad@playnext.local", "password": "demo12345", "genres": ["Simulation", "Adventure"]},
]


LEGACY_DEMO_USERNAMES = [
    "PixelWanderer",
    "FactoryOverlord",
    "QuestGoblin",
    "SuspiciousBarrel",
    "StealthIntern",
    "LaggingPhilosopher",
]


REVIEW_OVERRIDES = {
    "Hogwarts Legacy": [
        ("VoldemortFan69", 4, "The game is great... but why do not I have a nose after choosing a character?"),
        ("NapoleonTinyButMighty", 3, "Trolls attack suddenly, like the Russian frost in 1812."),
        ("GravityGuruNewton", 5, "Hogwarts completely ignores my laws, and somehow I still respect the castle."),
        ("StorySnack", 5, "I came to study magic and somehow got distracted by side quests for three hours."),
    ],
    "Baldur's Gate 3": [
        ("DemoPlayer", 5, "I came for one quest and stayed because every conversation turned into a surprise."),
        ("LoreLynx", 5, "Great writing, great characters, and just enough chaos to make every plan feel risky."),
        ("WeekendRanger", 5, "I meant to be serious, but the game kept rewarding my worst ideas."),
    ],
    "Cyberpunk 2077": [
        ("DemoPlayer", 4, "Night City looks great, sounds great, and keeps giving me one more thing to check."),
        ("MapMarkerMia", 5, "I opened the map for one mission and somehow found five more on the way."),
        ("NightShiftNina", 4, "Very stylish, very busy, and dangerously easy to keep playing late at night."),
    ],
    "Hades": [
        ("DemoPlayer", 5, "The game keeps defeating me in a very motivating way."),
        ("CouchCoopMax", 5, "Every run feels fast, clear, and just different enough to try one more time."),
        ("RacingToast", 4, "I said 'last run' three times and the game ignored me every time."),
    ],
    "Red Dead Redemption 2": [
        ("DemoPlayer", 5, "I tried to follow the story and got distracted by scenery, horses, and side activities."),
        ("WeekendRanger", 5, "Very easy to lose an hour just riding around and looking at the world."),
        ("PixelArchivist", 4, "Slow in a good way. It gives the world time to feel real."),
    ],
    "The Witcher 3: Wild Hunt": [
        ("DemoPlayer", 5, "I wanted to hunt one monster and somehow spent an hour helping strangers and playing cards. Very dangerous game for my schedule."),
        ("LoreLynx", 5, "Excellent quests, strong atmosphere, and a world that keeps pulling you off the main path."),
        ("TacticalTanya", 4, "I came for the monsters and stayed because even the side missions were interesting."),
    ],
}


GENERIC_REVIEWERS = [
    "CozyNomad",
    "MapMarkerMia",
    "LateShiftLeo",
    "StorySnack",
    "WeekendRanger",
    "NightShiftNina",
    "CouchCoopMax",
    "TacticalTanya",
    "RacingToast",
    "PixelArchivist",
    "SeaLevelSue",
    "LoreLynx",
]


GENERIC_REVIEW_TEXTS = [
    (5, "Very easy to recommend. I planned a short session and stayed much longer than expected."),
    (4, "Good atmosphere, clear gameplay, and enough variety to keep it interesting."),
    (4, "Fun overall. I kept saying 'one more mission' and the game kept winning that argument."),
    (5, "Strong first impression and a very comfortable gameplay loop."),
    (3, "Not everything worked for me, but I still had a decent time with it."),
    (4, "Looks good, plays smoothly, and never felt boring."),
    (5, "I opened it for a quick test and forgot what time it was."),
    (4, "A solid choice when you want something easy to get into after a long day."),
    (4, "The game has enough personality to stay fun even when I was not playing perfectly."),
    (5, "I came in curious and left fully convinced."),
    (3, "A bit uneven for me, but there is still plenty here to like."),
    (4, "It kept giving me a reason to continue, which is usually a very good sign."),
]


EXTRA_REVIEW_SEEDS = [
    {"game": "Stardew Valley", "username": "DemoPlayer", "rating": 5, "content": "I only wanted a calm farming game and somehow developed a full calendar, social strategy, and emotional attachment to parsnips."},
]


DEMO_VIEW_HISTORY = {
    "DemoPlayer": [
        "The Witcher 3: Wild Hunt",
        "Hades",
        "Red Dead Redemption 2",
    ]
}


def make_game_seed(title, cover_file, genres):
    if title in SPECIAL_TEXT:
        short_description, description, system_requirements = SPECIAL_TEXT[title]
    else:
        genre_text = ", ".join(genres[:3]).lower()
        short_description = f"A {genre_text} experience selected for players looking for a memorable session."
        description = (
            f"{title} brings together {genre_text} ideas with a clear hook, strong atmosphere, "
            "and enough personality to make it easy to discuss after playing. It is a good pick "
            "when you want something recognizable, stylish, and fun to compare with other games in the library."
        )
        storage = "20 GB"
        if "Open World" in genres:
            storage = "70 GB"
        elif "Shooter" in genres:
            storage = "50 GB"
        elif "Horror" in genres:
            storage = "15 GB"
        system_requirements = requirements(storage=storage)

    description = PAGE_DESCRIPTION_OVERRIDES.get(title, description)

    return {
        "title": title,
        "short_description": short_description,
        "description": description,
        "system_requirements": system_requirements,
        "cover_path": f"/covers/{cover_file}",
        "genres": genres,
    }


GAME_SEEDS = [make_game_seed(title, cover_file, genres) for title, cover_file, genres in GAME_CATALOG]


def build_review_seeds():
    review_seeds = []
    for index, game_seed in enumerate(GAME_SEEDS):
        title = game_seed["title"]
        if title in REVIEW_OVERRIDES:
            for username, rating, content in REVIEW_OVERRIDES[title]:
                review_seeds.append({"game": title, "username": username, "rating": rating, "content": content})
            continue

        for offset in range(3):
            username = GENERIC_REVIEWERS[(index + offset) % len(GENERIC_REVIEWERS)]
            rating, content = GENERIC_REVIEW_TEXTS[(index * 2 + offset) % len(GENERIC_REVIEW_TEXTS)]
            review_seeds.append({"game": title, "username": username, "rating": rating, "content": content})

    review_seeds.extend(EXTRA_REVIEW_SEEDS)
    return review_seeds


REVIEW_SEEDS = build_review_seeds()


def seed_database(db):
    genre_by_name = {}
    for genre_name in GENRE_NAMES:
        genre = db.query(Genre).filter(Genre.name == genre_name).first()
        if genre is None:
            genre = Genre(name=genre_name)
            db.add(genre)
        genre_by_name[genre_name] = genre

    db.flush()

    game_by_title = {}
    for game_seed in GAME_SEEDS:
        game = db.query(Game).filter(Game.title == game_seed["title"]).first()
        if game is None:
            game = Game(title=game_seed["title"])
            db.add(game)

        game.short_description = game_seed["short_description"]
        game.description = game_seed["description"]
        game.system_requirements = game_seed["system_requirements"]
        game.cover_path = game_seed["cover_path"]
        game.genres = [genre_by_name[name] for name in game_seed["genres"]]
        game_by_title[game_seed["title"]] = game

    db.flush()

    legacy_users = db.query(User).filter(User.username.in_(LEGACY_DEMO_USERNAMES)).all()
    for legacy_user in legacy_users:
        db.delete(legacy_user)

    db.flush()

    user_by_username = {}
    for user_seed in DEMO_USERS:
        user = (
            db.query(User)
            .filter((User.email == user_seed["email"]) | (User.username == user_seed["username"]))
            .first()
        )
        if user is None:
            user = User(
                username=user_seed["username"],
                email=user_seed["email"],
                password_hash=hash_password(user_seed["password"]),
                role="player",
            )
            db.add(user)
        else:
            user.username = user_seed["username"]
            user.email = user_seed["email"]
            user.password_hash = hash_password(user_seed["password"])
            user.role = "player"

        user.favorite_genres = [genre_by_name[name] for name in user_seed["genres"]]
        user_by_username[user_seed["username"]] = user

    db.flush()

    for review_seed in REVIEW_SEEDS:
        game = game_by_title[review_seed["game"]]
        user = user_by_username[review_seed["username"]]

        rating = (
            db.query(Rating)
            .filter(Rating.user_id == user.id, Rating.game_id == game.id)
            .first()
        )
        if rating is None:
            rating = Rating(user_id=user.id, game_id=game.id)
            db.add(rating)
        rating.value = review_seed["rating"]
        rating.updated_at = datetime.utcnow()

        review = (
            db.query(Review)
            .filter(Review.user_id == user.id, Review.game_id == game.id)
            .first()
        )
        if review is None:
            review = Review(user_id=user.id, game_id=game.id)
            db.add(review)
        review.content = review_seed["content"]
        review.updated_at = datetime.utcnow()

        existing_log = (
            db.query(ActivityLog)
            .filter(
                ActivityLog.user_id == user.id,
                ActivityLog.action == "seed_review",
                ActivityLog.details == game.title,
            )
            .first()
        )
        if existing_log is None:
            db.add(ActivityLog(user_id=user.id, action="seed_review", details=game.title))

    for username, viewed_titles in DEMO_VIEW_HISTORY.items():
        user = user_by_username[username]
        for title in viewed_titles:
            existing_view = (
                db.query(ActivityLog)
                .filter(
                    ActivityLog.user_id == user.id,
                    ActivityLog.action == "view_game",
                    ActivityLog.details == title,
                )
                .first()
            )
            if existing_view is None and title in game_by_title:
                db.add(ActivityLog(user_id=user.id, action="view_game", details=title))

    db.commit()
