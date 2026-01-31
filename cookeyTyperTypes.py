from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, TypedDict, Union


type EffectTarget = "FacilityTypes | Literal['Global'] | Literal['Click']"


class CookieSource(Enum):
    ELSE = 1
    TYPING = 2
    FACILITY = 3
    FACILITY_PURCHASE = 4
    UPGRADE_PURCHASE = 5


class VisualState(Enum):
    SHOWN = 1
    COVERED = 2
    HIDDEN = 3


class FacilityTypes(Enum):
    KEYBOARD = auto()
    GRANDMA = auto()
    FARM = auto()
    MINE = auto()
    FACTORY = auto()
    BANK = auto()
    TEMPLE = auto()
    WIZARD_TOWER = auto()
    SHIPMENT = auto()
    ALCHEMY_LAB = auto()
    PORTAL = auto()
    TIME_MACHINE = auto()
    ANTIMATTER_CONDENSER = auto()
    PRISM = auto()
    CHANCE_MAKER = auto()
    FRACTAL_ENGINE = auto()
    PYTHON_CONSOLE = auto()
    IDLEVERSE = auto()
    CORTEX_BAKER = auto()
    YOU = auto()


class UpgradeTypes(Enum):
    REINFORCED_INDEX_FINGER = auto()
    CARPAL_TUNNEL_PREVENTION = auto()
    AMBIDEXTROUS = auto()
    THOUSAND_FINGERS = auto()
    MILLION_FINGERS = auto()
    BILLION_FINGERS = auto()
    TRILLION_FINGERS = auto()
    QUADRILLION_FINGERS = auto()
    QUINTILLION_FINGERS = auto()
    SEXTILLION_FINGERS = auto()
    SEPTILLION_FINGERS = auto()
    OCTILLION_FINGERS = auto()
    NONILLION_FINGERS = auto()
    DECILLION_FINGERS = auto()
    UNDECILLION_FINGERS = auto()
    FORWARD_FROM_GRANDMA = auto()
    STEEL_PLATED_ROLLING_PINS = auto()
    LUBRICATED_DENTURES = auto()
    PRUNE_JUICE = auto()
    DOUBLE_THICK_GLASSES = auto()
    AGING_AGENTS = auto()
    XTREME_WALKERS = auto()
    THE_UNBRIDLING = auto()
    REVERSE_DEMENTIA = auto()
    TIMEPROOF_HAIR_DYES = auto()
    GOOD_MANNERS = auto()
    GENERATION_DEGENERATION = auto()
    VISITS = auto()
    KITCHEN_CABINETS = auto()
    FOAM_TIPPED_CANES = auto()
    CHEAP_HOES = auto()
    FERTILIZER = auto()
    COOKIE_TREES = auto()
    GENETICALLY_MODIFIED_COOKIES = auto()
    GINGERBREAD_SCARECROWS = auto()
    PULSAR_SPRINKLERS = auto()
    FUDGE_FUNGUS = auto()
    WHEAT_TRIFFIDS = auto()
    HUMANE_PESTICIDES = auto()
    BARNSTARS = auto()
    LINDWORMS = auto()
    GLOBAL_SEED_VAULT = auto()
    REVERSE_SEASONS = auto()
    FARM_AUTOMATION = auto()
    SUGAR_GAS = auto()
    MEGADRILL = auto()
    ULTRADRILL = auto()
    ULTIMADRILL = auto()
    H_BOMB_MINING = auto()
    COREFORGE = auto()
    PLANETSPLITTERS = auto()
    CANOLA_OIL_WELLS = auto()
    MOLE_PEOPLE = auto()
    MINE_CANARIES = auto()
    BORE_AGAIN = auto()
    MOUNTAIN_MACAROONS = auto()
    MINE_MILK = auto()
    MINE_AUTOMATION = auto()
    STURDIER_CONVEYOR_BELTS = auto()
    CHILD_LABOR = auto()
    SWEATSHOP = auto()
    RADIUM_REACTORS = auto()
    RECOMBOBULATORS = auto()
    DEEP_BOP = auto()
    CYBORG_WORKFORCE = auto()
    DRONE_HIVE = auto()
    FACTORY_CANARIES = auto()
    FACTORY_AUTOMATION = auto()
    FULLFILLING_COOKIES = auto()
    COOKIE_CRUMBS_RECYCLING = auto()
    FACTORY_AUTOMATION_2 = auto()
    TALLER_TELLERS = auto()
    SCISSOR_RESISTANT_CREDIT_CARDS = auto()
    ACID_PROOF_VAULTS = auto()
    CHOCOLATE_COINS = auto()
    EXPONENTIAL_INTEREST_RATES = auto()
    FINANCIAL_ZEN = auto()
    WAY_OF_THE_WALLET = auto()
    THE_STIMULUS_PACKAGE = auto()
    BUDGET_CAPS = auto()
    COOKIE_BANKS = auto()
    MEGABANKS = auto()
    BANK_AUTOMATION = auto()
    INSURANCE_FRAUD = auto()
    BANK_OF_BANKS = auto()
    GOLDEN_IDOLS = auto()
    SACRIFICES = auto()
    DELICIOUS_BLESSING = auto()
    SUN_FESTIVAL = auto()
    ENLARGED_PANTHEON = auto()
    GREAT_BAKER_IN_THE_SKY = auto()
    CREATION_MYTH = auto()
    THEOCRACY = auto()
    SICK_BEATS = auto()
    TEMPLE_CANARIES = auto()
    TEMPLE_AUTOMATION = auto()
    DEVOTED_FOLLOWERS = auto()
    THE_FINAL_SACRIFICE = auto()
    POINTIER_HATS = auto()
    BEARDIER_BEARDS = auto()
    ANCIENT_GRIMOIRES = auto()
    KITCHEN_CURSORS = auto()
    SCHOOL_OF_SORCERY = auto()
    DARK_FORMULAS = auto()
    COOKIEMANCY = auto()
    RABBIT_TRICK = auto()
    DELUXE_TAILORED_WANDS = auto()
    WHOOPEE_CUSHION = auto()
    WIZARD_AUTOMATION = auto()
    MAGIC_SHROOMS = auto()
    THE_ULTIMATE_CLICKSPORT = auto()
    VANILLA_NEBULAE = auto()
    WORMHOLES = auto()
    FREQUENT_FLYER = auto()
    WARP_DRIVE = auto()
    CHOCOLATE_MONOLITHS = auto()
    GENERATION_SHIP = auto()
    DYSON_SPHERE = auto()
    THE_FINAL_FRONTIER = auto()
    AUTOPILOT = auto()
    SHIPMENT_AUTOMATION = auto()
    SHIPMENT_REUSABILITY = auto()
    THE_COSMIC_BAKER = auto()
    ANTIMONY = auto()
    ESSENCE_OF_DOUGH = auto()
    TRUE_CHOCOLATE = auto()
    AMBROSIA = auto()
    AQUA_CRUSTULAE = auto()
    ORIGIN_CRUCIBLE = auto()
    THEORY_OF_ATOMIC_FLUIDITY = auto()
    BEIGE_GOO = auto()
    THE_PHILOSOPHERS_COOKIE = auto()
    ALCHEMY_AUTOMATION = auto()
    THE_MIDAS_TOUCH = auto()
    BEYOND_GOLD = auto()
    ANCIENT_TABLET = auto()
    INSANE_OATLING_WORKERS = auto()
    SOUL_BOND = auto()
    SANITY_DANCE = auto()
    BRANE_TRANSPLANT = auto()
    DEITY_SIZED_PORTALS = auto()
    END_OF_TIMES_BACK_UP_PLAN = auto()
    MADDENING_CHANTS = auto()
    THE_REAL_WORLD = auto()
    PORTAL_AUTOMATION = auto()
    PORTAL_MAINTENANCE = auto()
    COOKIE_DIMENSION = auto()
    FLUX_CAPACITORS = auto()
    TIME_PARADOX_RESOLVER = auto()
    QUANTUM_CONUNDRUM = auto()
    CAUSALITY_ENFORCER = auto()
    YESTERMORROW_COMPARATORS = auto()
    FAR_FUTURE_ENACTMENT = auto()
    GREAT_LOOP_HYPOTHESIS = auto()
    COOKIETOPIAN_MOMENTS_OF_MAYBE = auto()
    SECOND_SECONDS = auto()
    TIME_MACHINE_AUTOMATION = auto()
    NOSTALGIA_TRIP = auto()
    EPOCH_MANIPULATION = auto()
    SUGAR_BOSONS = auto()
    STRING_THEORY = auto()
    LARGE_MACARON_COLLIDER = auto()
    BIG_BANG_BAKE = auto()
    REVERSE_CYCLOTRONS = auto()
    NANOCOSMICS = auto()
    THE_PULSE = auto()
    SOME_OTHER_SUPER_PARTICLE = auto()
    QUANTUM_OVENPROOFING = auto()
    ANTIMATTER_AUTOMATION = auto()
    PRIMORDIAL_PARTICLE = auto()
    ANTI_UNIVERSE = auto()
    GEM_POLISH = auto()
    NINTH_COLOR = auto()
    CHOCOLATE_LIGHT = auto()
    GRAINBOW = auto()
    PURE_COSMIC_LIGHT = auto()
    GLOW_IN_THE_DARK = auto()
    LENSES_OF_TRUTH = auto()
    RECURSIVE_MIRRORS = auto()
    CRYSTAL_MEMORIES = auto()
    PRISM_AUTOMATION = auto()
    COLORBLIND_GLASSES = auto()
    SHIMMERING_HORIZON = auto()
    YOUR_LUCKY_COOKIE = auto()
    ALL_OR_NOTHING = auto()
    TURBOCHARGED_LUCK = auto()
    LUCKY_DIGITS = auto()
    LUCKY_PAYOUT = auto()
    LUCKY_FINGERS = auto()
    ENTANGLEMENT = auto()
    JUST_IN_TIME = auto()
    WAGER_WAR = auto()
    CHANCEMAKER_AUTOMATION = auto()
    LUCKY_GRANDMA = auto()
    THE_ULTIMATE_GAMBLE = auto()
    METABAKERIES = auto()
    MANDELBROWN_SUGAR = auto()
    FRACTOIDS = auto()
    NESTED_UNIVERSE_THEORY = auto()
    MENGER_SPONGE_CAKE = auto()
    ONE_PARTICULARLY_GOOD_INFINITY = auto()
    INFINITE_SUGARCUBES = auto()
    ENDLESS_BOOK_OF_PROSE = auto()
    DOUGH_BLOOMING = auto()
    FRACTAL_ENGINE_AUTOMATION = auto()
    DOUGHSCENSION = auto()
    RECURSIVE_DELICACIES = auto()
    ALERT_JS = auto()
    EVAL_JS = auto()
    TOSTRING_JS = auto()
    MOAR_MONEYS_JS = auto()
    ALGORITHM_GOODNESS = auto()
    SOURCE_CODE = auto()
    AUTOCOMPLETE = auto()
    AI_BAKERS = auto()
    SENTIENT_CODE = auto()
    CONSOLE_AUTOMATION = auto()
    MALWARE = auto()
    SUPERBUG = auto()
    MANIFEST_DESTINY = auto()
    THE_MULTIVERSE_IN_A_NUTSHELL = auto()
    ALL_CONSUMING = auto()
    ETERNAL_RECURSION = auto()
    PARA_REALITY_ADAPTATION = auto()
    HYPNODRONES = auto()
    DARK_MATTER_INTERFERENCE = auto()
    MULTIVERSE_MAYHEM = auto()
    LIGHT_SPEED_IDLEVERSE = auto()
    IDLEVERSE_AUTOMATION = auto()
    SELF_CONTAINED_REALITY = auto()
    ENDLESS_LOOP = auto()
    NEURAL_NETWORKS = auto()
    BRAIN_TRUST = auto()
    MEMORY_PALACES = auto()
    QUANTUM_MINDS = auto()
    SYNTHETIC_SYNAPSE = auto()
    COLLECTIVE_THINKING = auto()
    HIVE_MIND = auto()
    CORTEX_CONSCIOUSNESS = auto()
    BRAINSTORM = auto()
    CORTEX_AUTOMATION = auto()
    DREAM_BAKER = auto()
    PSYCHIC_COOKIES = auto()
    ME_MYSELF_AND_I = auto()
    SOUL_SEARCH = auto()
    EXISTENTIAL_COOKIES = auto()
    MINDFUL_BAKING = auto()
    INNER_STRENGTH = auto()
    ETERNAL_YOUTH = auto()
    SELF_DISCOVERY = auto()
    EXISTENTIAL_CRISIS = auto()
    THE_REAL_YOU = auto()
    YOU_AUTOMATION = auto()
    ENLIGHTENMENT = auto()
    GODHOOD = auto()


class ModifierSourceType(Enum):
    UPGRADE = auto()
    ACHIEVEMENT = auto()
    BUFF = auto()


class EffectType(Enum):
    ADD = auto()
    MULTIPLIER = auto()


class FacilityConfig(TypedDict):
    name: str
    description: str
    base_cost: int
    base_cps: float | int
    init_visual: VisualState


class UpgradeConfig(TypedDict):
    name: str
    description: str
    price: int
    target: FacilityTypes | Literal["Global"] | Literal["Click"]
    effect_type: EffectType
    value: float
    unlock_facility: FacilityTypes
    unlock_count: int


class Res(Enum):
    OK = 1
    ERR = 2


class Parameters(TypedDict):
    facility_cost_multiplier_by_amount: float
    tick_rate: int


# ----------   Commands   ----------


class Operations(Enum):
    INVALID_OPERATION_ERROR = 1
    BUY = 2
    SELL = 3
    DETAIL = 4
    LS = 5
    LA = 6


@dataclass
class CommandInvalidError:
    type: Literal["invalid"] = "invalid"


@dataclass
class CommandFacility:
    operation: Operations
    target: FacilityTypes | None = None
    type: Literal["facility"] = "facility"
    amount: int = 1


@dataclass
class CommandUpgrade:
    operation: Operations
    target: UpgradeTypes | None = None
    type: Literal["upgrade"] = "upgrade"


@dataclass
class CommandHelp:
    type: Literal["help"] = "help"


@dataclass
class CommandInspectCookieCount:
    type: Literal["cc"] = "cc"


@dataclass
class CommandInspectCookiePerSecond:
    type: Literal["cps"] = "cps"


@dataclass
class CommandInspectCookiePerType:
    type: Literal["cpt"] = "cpt"


@dataclass
class CommandUserInput:
    type: Literal["input"] = "input"
    content: str = ""


Command = Union[
    CommandInvalidError,
    CommandFacility,
    CommandUpgrade,
    CommandHelp,
    CommandInspectCookieCount,
    CommandInspectCookiePerSecond,
    CommandInspectCookiePerType,
    CommandUserInput,
]
