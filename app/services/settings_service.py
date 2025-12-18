from sqlalchemy.orm import Session
from app.models.setting import SystemSetting
from typing import Any, List, Dict

from app.api.deps import SessionDep
from app.core.settings_loader import invalidate_settings_cache

class SettingsService:
    def __init__(self, db: SessionDep):
        self.db = db

    # --- DEFINITIONS ---
    # Define defaults here. The app will ensure these exist on startup.
    DEFAULTS = [
        {
            "key": "general.app_name", "value": "Parker Comic Server",
            "description": "Add a prefix to the server name",
            "category": "general", "data_type": "string",
            "label": "Application Name"
        },
        {
            "key": "scanning.batch_window", "value": "600",
            "category": "scanning", "data_type": "int",
            "label": "Scan Batch Window (Sec)",
            "description": "Time to wait for file operations to settle."
        },
        {
            "key": "ui.login_background_style", "value": "none",
            "category": "appearance", "data_type": "select",
            "label": "Login Background Style",
            "description": "Choose what appears behind the login form.",
            "options": [
                {"label": "None (Gradient only)", "value": "none"},
                {"label": "Random library covers", "value": "random_covers"},
                {"label": "Solid Color", "value": "solid_color"},
                {"label": "Static Cover", "value": "static_cover"}
            ]
        },
        {
            "key": "ui.login_solid_color",
            "value": "superman_classic",
            "category": "appearance",
            "data_type": "select",
            "label": "Login Solid Color",
            "description": "Choose a color gradient.",
            "depends_on": { "key": "ui.login_background_style", "value": "solid_color" },
            "options": [
                # DC Heroes
                {"label": "Superman Classic", "value": "superman_classic", "group": "DC Heroes"},
                {"label": "Wonder Woman", "value": "wonder_woman", "group": "DC Heroes"},
                {"label": "Batman Gotham", "value": "batman_gotham", "group": "DC Heroes"},
                {"label": "Nightwing", "value": "nightwing_blue", "group": "DC Heroes"},
                {"label": "Robin Traffic Light", "value": "robin_traffic", "group": "DC Heroes"},
                {"label": "Red Hood", "value": "red_hood", "group": "DC Heroes"},
                {"label": "Batgirl/Oracle", "value": "batgirl_purple", "group": "DC Heroes"},
                {"label": "Batwoman", "value": "batwoman_crimson", "group": "DC Heroes"},
                {"label": "Green Arrow", "value": "green_arrow", "group": "DC Heroes"},
                {"label": "Kryptonian Blue (Superman)", "value": "kryptonian_blue", "group": "DC Heroes"},
                {"label": "Shazam", "value": "shazam_thunder", "group": "DC Heroes"},
                {"label": "Blue Beetle", "value": "blue_beetle", "group": "DC Heroes"},
                {"label": "Booster Gold", "value": "booster_gold", "group": "DC Heroes"},
                {"label": "Cyborg", "value": "cyborg_tech", "group": "DC Heroes"},
                {"label": "Scarlet Speedster (Flash)", "value": "scarlet_speedster", "group": "DC Heroes"},
                {"label": "Stargirl", "value": "stargirl", "group": "DC Heroes"},
                {"label": "Hawkman", "value": "hawkman_wings", "group": "DC Heroes"},
                {"label": "Martian Manhunter", "value": "martian_manhunter", "group": "DC Heroes"},
                {"label": "Teen Titans", "value": "teen_titans", "group": "DC Heroes"},

                # Marvel Heroes
                {"label": "Hulk Gamma", "value": "hulk_gamma", "group": "Marvel Heroes"},
                {"label": "Iron Man Gold", "value": "iron_gold", "group": "Marvel Heroes"},
                {"label": "Mjolnir Silver (Thor)", "value": "mjolnir_silver", "group": "Marvel Heroes"},
                {"label": "Wakanda Purple (Black Panther)", "value": "wakanda_purple", "group": "Marvel Heroes"},
                {"label": "Spider-Gwen", "value": "spider_gwen", "group": "Marvel Heroes"},
                {"label": "Nova Corps", "value": "nova_corps", "group": "Marvel Heroes"},
                {"label": "Daredevil Red", "value": "daredevil_red", "group": "Marvel Heroes"},
                {"label": "Nightcrawler", "value": "nightcrawler", "group": "Marvel Heroes"},
                {"label": "X-Men Gold", "value": "x_men_gold", "group": "Marvel Heroes"},

                # DC Villains
                {"label": "Joker Madness", "value": "joker_madness", "group": "DC Villains"},
                {"label": "Harley Chaos", "value": "harley_chaos", "group": "DC Villains"},
                {"label": "Lex Luthor", "value": "lex_luthor", "group": "DC Villains"},
                {"label": "Darkseid", "value": "darkseid_omega", "group": "DC Villains"},
                {"label": "Brainiac", "value": "brainiac", "group": "DC Villains"},
                {"label": "Deathstroke", "value": "deathstroke", "group": "DC Villains"},
                {"label": "Reverse Flash", "value": "reverse_flash", "group": "DC Villains"},
                {"label": "Sinestro", "value": "sinestro", "group": "DC Villains"},
                {"label": "Black Adam", "value": "black_adam", "group": "DC Villains"},
                {"label": "Killer Croc", "value": "killer_croc", "group": "DC Villains"},
                {"label": "Mr. Freeze", "value": "mr_freeze", "group": "DC Villains"},
                {"label": "The Riddler", "value": "riddler", "group": "DC Villains"},
                {"label": "Two-Face", "value": "two_face", "group": "DC Villains"},
                {"label": "The Penguin", "value": "penguin", "group": "DC Villains"},
                {"label": "Bane", "value": "bane_venom", "group": "DC Villains"},

                # Marvel Villains & Anti-Heroes
                {"label": "Venom Black", "value": "venom_black", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Symbiote Swirl", "value": "symbiote_swirl", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Carnage Chaos", "value": "carnage_chaos", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Deadpool Merc", "value": "deadpool_merc", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Green Goblin", "value": "green_goblin", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Magneto Master", "value": "magneto_master", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Punisher Skull", "value": "punisher_skull", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Ghost Rider Flame", "value": "ghost_rider", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Elektra Crimson", "value": "elektra_crimson", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Poison Ivy", "value": "poison_ivy", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Mystique Blue", "value": "mystique_blue", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Thanos Titan", "value": "thanos_titan", "group": "Marvel Villains & Anti-Heroes"},
                {"label": "Apocalypse", "value": "apocalypse", "group": "Marvel Villains & Anti-Heroes"},

                # Lantern Corps
                {"label": "Green Lantern (Will)", "value": "lantern_green", "group": "Lantern Corps"},
                {"label": "Red Lantern (Rage)", "value": "red_lantern", "group": "Lantern Corps"},
                {"label": "Blue Lantern (Hope)", "value": "blue_lantern", "group": "Lantern Corps"},
                {"label": "Sinestro Corps (Fear)", "value": "sinestro_corps", "group": "Lantern Corps"},
                {"label": "Star Sapphire (Love)", "value": "star_sapphire", "group": "Lantern Corps"},
                {"label": "Indigo Tribe (Compassion)", "value": "indigo_tribe", "group": "Lantern Corps"},
                {"label": "Agent Orange (Avarice)", "value": "agent_orange", "group": "Lantern Corps"},
                {"label": "White Lantern (Life)", "value": "white_lantern", "group": "Lantern Corps"},
                {"label": "Black Lantern (Death)", "value": "black_lantern", "group": "Lantern Corps"},

                # DC Dark/Mystical
                {"label": "Zatanna", "value": "zatanna_magic", "group": "DC Dark/Mystical"},
                {"label": "Constantine", "value": "constantine_trench", "group": "DC Dark/Mystical"},
                {"label": "Swamp Thing", "value": "swamp_thing", "group": "DC Dark/Mystical"},
                {"label": "Sandman (Dream)", "value": "sandman_dream", "group": "DC Dark/Mystical"},
                {"label": "Rorschach", "value": "rorschach", "group": "DC Dark/Mystical"},
                {"label": "Dr. Manhattan", "value": "dr_manhattan", "group": "DC Dark/Mystical"},

                # Cosmic & Special
                {"label": "Phoenix Force", "value": "phoenix_force", "group": "Cosmic & Special"},
                {"label": "Doctor Strange", "value": "doctor_strange", "group": "Cosmic & Special"},
                {"label": "Silver Surfer", "value": "silver_surfer", "group": "Cosmic & Special"},
                {"label": "Galactus Cosmic", "value": "galactus_cosmic", "group": "Cosmic & Special"},
                {"label": "Iron Patriot", "value": "iron_patriot", "group": "Cosmic & Special"},
                {"label": "Cosmic Entity", "value": "cosmic_entity", "group": "Cosmic & Special"},
                {"label": "Infinity Stones", "value": "infinity_stones", "group": "Cosmic & Special"},

                # DC Teams
                {"label": "Justice League", "value": "justice_league", "group": "DC Teams"},
                {"label": "Suicide Squad", "value": "suicide_squad", "group": "DC Teams"},
                {"label": "Birds of Prey", "value": "birds_of_prey", "group": "DC Teams"},

                # Other
                {"label": "Waverider Yellow", "value": "waverider_yellow", "group": "Other"},
                {"label": "Atlantis Teal (Aquaman)", "value": "atlantis_teal", "group": "Other"},
                {"label": "Gotham Night (Batman)", "value": "gotham_night", "group": "Other"},
            ]
        },
        {
            "key": "ui.login_static_cover",
            "value": "amazing-fantasy-15.jpg",
            "category": "appearance",
            "data_type": "select",
            "label": "Login Static Cover",
            "description": "Choose an iconic comic cover.",
            "depends_on": { "key": "ui.login_background_style", "value": "static_cover" },
            "options": [
                {"label": "Action Comics #1 (Superman)", "value": "action-comics-1.jpg" },
                {"label": "Amazing Fantasy #15 (Spider-Man)", "value": "amazing-fantasy-15.jpg" },
                {"label": "Amazing Spider-Man #121", "value": "amazing-spider-man-121.jpg" },
                {"label": "Amazing Spiderman #300", "value": "amazing-spiderman-300.jpg" },
                {"label": "Avengers #1", "value": "avengers-1.jpg" },
                {"label": "Avengers #4 (Captain America)", "value": "avengers-4.jpg" },
                {"label": "Batman #227", "value": "batman-227.jpg" },
                {"label": "Crisis on Infinite Earths #1", "value": "crisis-infinite-earths-1.jpg" },
                {"label": "Dark Knight Returns #1", "value": "dark-knight-returns-1.jpg" },
                {"label": "Detective Comics #27 (Batman)", "value": "detective-comics-27.jpg" },
                {"label": "Fantastic Four #1", "value": "fantastic-four-1.jpg" },
                {"label": "Giant Size X-Men #1", "value": "giant-size-x-men-1.jpg" },
                {"label": "Incredible Hulk #1", "value": "incredible-hulk-1.jpg" },
                {"label": "Iron Man #1", "value": "iron-man-1.jpg" },
                {"label": "Mister X #1", "value": "mister-x-1.jpg" },
                {"label": "Spawn #1", "value": "spawn-1.jpg" },
                {"label": "Spiderman #1", "value": "spiderman-1.jpg" },
                {"label": "Superman v2 #75", "value": "superman-75.jpg" },
                {"label": "Uncanny X-Men #141", "value": "uncanny-x-men-141.jpg" },
                {"label": "Watchmen #1", "value": "watchmen-1.jpg" },
                {"label": "X-Men #1", "value": "x-men-1.jpg" },
            ]
        },

        {
            "key": "ui.background_style", "value": "NONE",
            "category": "appearance", "data_type": "select",
            "label": "Background Style",
            "options": [
                {"label": "No background style", "value": "NONE"},
                {"label": "Hero backdrop style", "value": "HERO"},
                {"label": "Colorscape style (Plex)", "value": "COLORSCAPE"},
                {"label": "Colorscape with Hero overlay", "value": "HYBRID"},
            ]
        },
        {
            "key": "ui.pagination_mode",
            "value": "infinite",
            "category": "appearance",
            "data_type": "select",
            "label": "Pagination Style",
            "description": "How lists of series / issues are loaded.",
            "options": [
                {"label": "Infinite Scroll (Load on scroll)", "value": "infinite"},
                {"label": "Classic (Page numbers)", "value": "classic"}
            ]
        },
        {
            "key": "ui.on_deck.staleness_weeks", "value": "4",
            "category": "appearance", "data_type": "int",
            "label": "On Deck Staleness (Weeks)",
            "description": "Hide 'Continue Reading' items if not touched for this many weeks. Set to 0 to disable."
        },
        {
            "key": "system.task.backup.interval",
            "value": "weekly",
            "category": "system",
            "data_type": "select",
            "label": "Auto-Backup Interval",
            "description": "How often to perform a full database backup.",
            "options": [
                {"label": "Daily", "value": "daily"},
                {"label": "Weekly", "value": "weekly"},
                {"label": "Monthly", "value": "monthly"},
                {"label": "Disabled", "value": "disabled"}
            ]
        },
        {
            "key": "system.task.cleanup.interval",
            "value": "monthly",
            "category": "system",
            "data_type": "select",
            "label": "Auto-Cleanup Interval",
            "description": "How often to clear orphaned metadata (unused characters, tags, etc).",
            "options": [
                {"label": "Daily", "value": "daily"},
                {"label": "Weekly", "value": "weekly"},
                {"label": "Monthly", "value": "monthly"}
            ]
        },
        {
            "key": "system.parallel_image_processing",
            "value": "false",
            "category": "system",
            "data_type": "bool",
            "label": "Enable Parallel Image Processing",
            "description": "Use all CPU cores to speed up thumbnail generation. May increase system load."
        },
        {
            "key": "system.parallel_image_workers",
            "value": "0",
            "category": "system",
            "data_type": "int",
            "label": "Parallel Image Worker Count",
            "description": "Number of worker processes for thumbnail generation. 0 = auto (use all CPU cores). Values above your CPU count will be clamped."
        },
        {
            "key": "system.task.scan.interval",
            "value": "daily",
            "category": "system",
            "data_type": "select",
            "label": "Scheduled Library Scan",
            "description": "Safety net scan for all libraries (useful if folder watching is unreliable).",
            "options": [
                {"label": "Daily", "value": "daily"},
                {"label": "Weekly", "value": "weekly"},
                {"label": "Disabled", "value": "disabled"}
            ]
        },

        {
            "key": "backup.retention_days", "value": "7",
            "category": "backup", "data_type": "int",
            "label": "Backup Retention (Days)"
        },
        {
            "key": "general.log_level",
            "value": "INFO",
            "category": "general",
            "data_type": "select",
            "label": "Logging Level",
            "description": "Server restart required for this change to take effect.",
            "options": [
                {"label": "Debug", "value": "DEBUG"},
                {"label": "Info", "value": "INFO"},
                {"label": "Warning", "value": "WARNING"},
                {"label": "Error", "value": "ERROR"},
            ]
        },
        {
            "key": "server.opds_enabled", "value": "false",
            "category": "server", "data_type": "bool",
            "label": "Enable OPDS Feed",
            "description": "Allows external readers (Chunky, Panels) to access library via /opds using Basic Auth."
        },


    ]

    def initialize_defaults(self):
        """
        Seeds default settings and updates metadata (labels, descriptions) for existing ones.
        Does NOT overwrite existing 'values' to preserve user configuration.
        """
        # 1. Fetch all existing settings mapped by key for fast lookup
        existing_settings = {
            s.key: s
            for s in self.db.query(SystemSetting).all()
        }

        for default in self.DEFAULTS:

            key = default["key"]

            if key not in existing_settings:
                # Case 1: New Setting -> Create it fully (including default value)
                obj = SystemSetting(**default)
                self.db.add(obj)
            else:
                # Case 2: Existing Setting -> Sync metadata only
                # We update definitions to match the code, but we generally
                # DO NOT touch 'value' so we don't overwrite user preferences.
                setting = existing_settings[key]

                # Update metadata fields
                setting.label = default.get("label")
                setting.description = default.get("description")
                setting.category = default.get("category")
                setting.data_type = default.get("data_type")

                # Update 'options' if your model supports it (JSON column)
                # This ensures new dropdown choices appear in the UI.
                if "options" in default:
                    setting.options = default["options"]

                if "depends_on" in default:
                    setting.depends_on = default["depends_on"]

                # NOTE: If we strictly needed to force-update a value (e.g. security patch),
                # we would need explicit logic here, but usually we leave .value alone.

        self.db.commit()

    def get_all_grouped(self) -> Dict[str, List[SystemSetting]]:
        """Returns settings grouped by category for the UI"""
        settings = self.db.query(SystemSetting).filter(SystemSetting.is_hidden == False).all()
        grouped = {}
        for s in settings:
            s.value = self._cast_value(s.value, s.data_type)  # Cast for API
            if s.category not in grouped:
                grouped[s.category] = []
            grouped[s.category].append(s)

        return grouped

    def get(self, key: str) -> Any:
        """Get a single setting value (Casted)"""
        setting = self.db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if not setting:
            return None
        return self._cast_value(setting.value, setting.data_type)

    def update(self, key: str, value: Any) -> SystemSetting:
        setting = self.db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if not setting:
            raise ValueError("Setting not found")

        # Convert to string for storage
        if setting.data_type == "bool":
            setting.value = str(value).lower()  # "true"/"false"
        else:
            setting.value = str(value)

        self.db.commit()
        self.db.refresh(setting)

        # Clear the read-cache so the app sees the change immediately
        invalidate_settings_cache()

        return setting

    def _cast_value(self, value: str, data_type: str) -> Any:
        """Convert DB String -> Python Type"""
        if value is None: return None
        if data_type == "int":
            return int(value)
        if data_type == "bool":
            return value.lower() in ('true', '1', 't', 'yes')
        return value