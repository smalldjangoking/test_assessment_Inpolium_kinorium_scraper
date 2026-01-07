from enum import IntEnum, Enum

class PerPageLimit(IntEnum):
    """Available limits for 'per_page' parameter"""
    SMALL = 50
    MEDIUM = 100
    LARGE = 200


from enum import Enum

class Genre(str, Enum):
    """
    Movies genre list of kinorium.com.
    Swagger displays the names, while the .id property provides the site's internal ID.
    """
    ANIME = "Anime"
    ACTION = "Action"
    WESTERN = "Western"
    WAR = "War"
    MYSTERY = "Mystery"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    CRIME = "Crime"
    ROMANCE = "Romance"
    ANIMATION = "Animation"
    MUSICAL = "Musical"
    ADVENTURE = "Adventure"
    FAMILY = "Family"
    THRILLER = "Thriller"
    HORROR = "Horror"
    SCI_FI = "Sci-Fi"
    FILM_NOIR = "Film Noir"
    FANTASY = "Fantasy"
    BIOGRAPHY = "Biography"
    DOCUMENTARY = "Documentary"
    HISTORY = "History"
    MUSIC = "Music"
    SPORT = "Sport"
    GAME_SHOW = "Game Show"
    CONCERT = "Concert"
    SHORT = "Short"
    NEWS = "News"
    REALITY_TV = "Reality TV"
    TALK_SHOW = "Talk Show"
    AWARD = "Award"

    @property
    def id(self) -> int:
        """Returns the internal ID used by kinorium.com for the genre filter."""
        mapping = {
            Genre.ANIME: 1,
            Genre.BIOGRAPHY: 2,
            Genre.ACTION: 3,
            Genre.WESTERN: 4,
            Genre.WAR: 5,
            Genre.MYSTERY: 6,
            Genre.DOCUMENTARY: 9,
            Genre.DRAMA: 10,
            Genre.GAME_SHOW: 11,
            Genre.HISTORY: 12,
            Genre.COMEDY: 13,
            Genre.CONCERT: 14,
            Genre.SHORT: 15,
            Genre.CRIME: 16,
            Genre.ROMANCE: 17,
            Genre.MUSIC: 18,
            Genre.ANIMATION: 19,
            Genre.MUSICAL: 20,
            Genre.NEWS: 21,
            Genre.ADVENTURE: 22,
            Genre.REALITY_TV: 23,
            Genre.FAMILY: 24,
            Genre.SPORT: 25,
            Genre.TALK_SHOW: 26,
            Genre.THRILLER: 27,
            Genre.HORROR: 28,
            Genre.SCI_FI: 29,
            Genre.FILM_NOIR: 30,
            Genre.FANTASY: 31,
            Genre.AWARD: 32,
        }
        return mapping.get(self, 31) # Default to FANTASY ID if not found