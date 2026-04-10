from datetime import datetime

from .auth import hash_password
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
    ("Amnesia: A Machine for Pigs", "Amnesia_A_Machine_For_Pigs.jpg", ["Horror", "Adventure", "Story Rich"]),
    ("Amnesia: Rebirth", "Amnesia_Rebirth.jpg", ["Horror", "Adventure", "Story Rich"]),
    ("Amnesia: The Bunker", "Amnesia_The_Bunker.jpg", ["Horror", "Survival", "Stealth"]),
    ("Amnesia: The Dark Descent", "Amnesia_The_Dark_Descent.jpg", ["Horror", "Survival", "Classic"]),
    ("Assassin's Creed Unity", "Assasin_s_Creed_Unity.jpg", ["Action", "Adventure", "Open World", "Stealth"]),
    ("Batman: Arkham Asylum", "Batman_Arkham_Asylum.jpg", ["Action", "Adventure", "Superhero"]),
    ("Batman: Arkham City", "Batman_Arkham_City.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Batman: Arkham Knight", "Batman_Arkham_Knight.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Batman: Arkham Origins", "Batman_Arkham_Origins.jpg", ["Action", "Adventure", "Superhero"]),
    ("Battlefield 1 Revolution", "Battlefield_1_Revolution.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("Battlefield 4", "Battlefield_4.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("Battlefield V", "Battlefield_V.jpg", ["Shooter", "Action", "Multiplayer"]),
    ("BioShock 2", "Bioshock_2.jpg", ["Shooter", "Story Rich", "Action"]),
    ("Buckshot Roulette", "Buckshot_Roulette.jpg", ["Horror", "Strategy"]),
    ("Chained Together", "Chained_together.jpg", ["Co-op", "Adventure", "Puzzle"]),
    ("Counter-Strike 2", "Counter_Strike_2.jpg", ["Shooter", "Competitive", "Action"]),
    ("Darkwood", "Darkwood.jpg", ["Horror", "Survival", "Story Rich"]),
    ("Dota 2", "Dota_2.jpg", ["MOBA", "Competitive", "Strategy"]),
    ("Factorio", "Factorio.jpg", ["Strategy", "Simulation"]),
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
    ("Resident Evil 0", "Resident_Evil_0.jpg", ["Horror", "Survival", "Classic"]),
    ("Resident Evil 2", "Resident_Evil_2.jpg", ["Horror", "Survival", "Action"]),
    ("Resident Evil 4", "Resident_Evil_4.jpg", ["Horror", "Action", "Survival"]),
    ("Rise of the Tomb Raider", "Rise_of_the_Tomb_Raider.jpg", ["Action", "Adventure", "Puzzle"]),
    ("Rust", "Rust.jpg", ["Survival", "Open World", "Co-op"]),
    ("Spider-Man Remastered", "Spider_man_Remastered.jpg", ["Action", "Adventure", "Superhero", "Open World"]),
    ("Terraria", "Terraria.jpg", ["Adventure", "Survival", "Co-op"]),
    ("That Which Gave Chase", "That_Which_Gave_Chase.jpg", ["Horror", "Adventure"]),
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
}


DEMO_USERS = [
    {"username": "VoldemortFan69", "email": "voldemortfan69@playnext.local", "password": "demo12345", "genres": ["RPG", "Adventure"]},
    {"username": "NapoleonTinyButMighty", "email": "napoleon@playnext.local", "password": "demo12345", "genres": ["Strategy", "Action"]},
    {"username": "GravityGuruNewton", "email": "newton@playnext.local", "password": "demo12345", "genres": ["Puzzle", "Story Rich"]},
    {"username": "PixelWanderer", "email": "pixel@playnext.local", "password": "demo12345", "genres": ["Adventure", "Open World"]},
    {"username": "FactoryOverlord", "email": "factory@playnext.local", "password": "demo12345", "genres": ["Strategy", "Simulation"]},
    {"username": "QuestGoblin", "email": "goblin@playnext.local", "password": "demo12345", "genres": ["RPG", "Open World"]},
    {"username": "SuspiciousBarrel", "email": "barrel@playnext.local", "password": "demo12345", "genres": ["Horror", "Puzzle"]},
    {"username": "StealthIntern", "email": "stealth@playnext.local", "password": "demo12345", "genres": ["Stealth", "Action"]},
    {"username": "LaggingPhilosopher", "email": "lag@playnext.local", "password": "demo12345", "genres": ["Competitive", "Shooter"]},
]


REVIEW_OVERRIDES = {
    "Hogwarts Legacy": [
        ("VoldemortFan69", 4, "The game is great... but why do not I have a nose after choosing a character?"),
        ("NapoleonTinyButMighty", 3, "Trolls attack suddenly, like the Russian frost in 1812."),
        ("GravityGuruNewton", 5, "Hogwarts completely ignores my laws, and somehow I still respect the castle."),
        ("QuestGoblin", 5, "I went to learn magic and accidentally enrolled in Inventory Management 101."),
    ],
    "Factorio": [
        ("FactoryOverlord", 5, "I installed it for one evening and left three days later with conveyor belts in my dreams."),
        ("GravityGuruNewton", 5, "The factory must grow. I am not sure who said it first, but I now obey."),
        ("QuestGoblin", 4, "Very relaxing, if your idea of relaxing is arguing with iron plates."),
    ],
    "Counter-Strike 2": [
        ("LaggingPhilosopher", 4, "I peeked mid and discovered both mortality and bad Wi-Fi."),
        ("NapoleonTinyButMighty", 5, "A tactical masterpiece, especially when everyone ignores the tactic."),
        ("StealthIntern", 4, "The enemy cannot see me if I miss every shot and confuse them emotionally."),
    ],
    "Portal 2": [
        ("GravityGuruNewton", 5, "Portals are illegal according to my paperwork, but I enjoyed the violation."),
        ("SuspiciousBarrel", 5, "The cake jokes aged better than most of my group projects."),
        ("PixelWanderer", 5, "Every puzzle made me feel smart exactly three seconds after feeling hopeless."),
    ],
    "Grand Theft Auto V": [
        ("NapoleonTinyButMighty", 5, "No plan survives contact with Los Santos traffic."),
        ("PixelWanderer", 4, "I started a mission and somehow spent an hour choosing a car I immediately crashed."),
        ("QuestGoblin", 4, "The city is so alive that even the sidewalks seem personally offended by me."),
    ],
    "Hitman World of Assassination": [
        ("StealthIntern", 5, "A perfect game for people who say 'I have a plan' and then use a fish."),
        ("PixelWanderer", 5, "Every mission makes me feel smart right before I accidentally knock out the wrong person."),
        ("SuspiciousBarrel", 4, "Disguises work so well that I am now suspicious of every waiter in real life."),
    ],
    "Prey": [
        ("GravityGuruNewton", 5, "I no longer trust coffee mugs, chairs, or the concept of safety."),
        ("SuspiciousBarrel", 5, "The mimics turned interior design into a survival mechanic."),
        ("FactoryOverlord", 4, "Great station. Terrible workplace safety policy."),
    ],
    "Rise of the Tomb Raider": [
        ("VoldemortFan69", 4, "The tombs are excellent. The cliffs clearly hate me, but the tombs are excellent."),
        ("QuestGoblin", 5, "I came for treasure and stayed because Lara has better cardio than my entire university group."),
        ("PixelWanderer", 4, "Very pretty snow, very rude enemies, excellent climbing."),
    ],
}


GENERIC_REVIEWS = [
    ("PixelWanderer", 4, "I opened it for a quick session and immediately lost track of time. Suspicious behavior from a game."),
    ("QuestGoblin", 5, "The side content keeps stealing my attention like it pays rent in my brain."),
    ("SuspiciousBarrel", 4, "I do not fully trust the level design, which probably means it is doing a good job."),
    ("StealthIntern", 4, "I tried to play carefully, failed loudly, and still had a great time."),
    ("LaggingPhilosopher", 3, "My skill level says no, but my confidence keeps pressing Play."),
    ("FactoryOverlord", 5, "The gameplay loop is dangerously comfortable. I respect it and fear it."),
    ("VoldemortFan69", 4, "Strong atmosphere, good pacing, and no one asked me about my nose. Perfect."),
    ("NapoleonTinyButMighty", 4, "The game has ambition. I respect ambition, especially when it does not invade Russia."),
    ("GravityGuruNewton", 5, "Physics occasionally disagrees with me, but entertainment wins this round."),
]


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
            username, rating, content = GENERIC_REVIEWS[(index + offset) % len(GENERIC_REVIEWS)]
            review_seeds.append({"game": title, "username": username, "rating": rating, "content": content})

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

    user_by_username = {}
    for user_seed in DEMO_USERS:
        user = db.query(User).filter(User.email == user_seed["email"]).first()
        if user is None:
            user = User(
                username=user_seed["username"],
                email=user_seed["email"],
                password_hash=hash_password(user_seed["password"]),
                role="player",
            )
            db.add(user)

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

    db.commit()
