from project.band import Band
from project.band_members.drummer import Drummer
from project.band_members.guitarist import Guitarist
from project.band_members.singer import Singer
from project.concert import Concert


band_musicians = {
    'drummer': 0,
    'singer': 0,
    'guitarist': 0
}


class ConcertTrackerApp:
    bands = []
    musicians = []
    concerts = []

    def get_concert_by_place(self, concert_place):
        for concert in self.concerts:
            if concert.place == concert_place:
                return concert
        return None

    def get_band_by_name(self, some_name):
        for b in self.bands:
            if b.name == some_name:
                return b
        return None

    def get_musician_by_name(self, some_name):
        for m in self.musicians:
            if m.name == some_name:
                return m
        return None

    def create_musician(self, musician_type: str, name: str, age: int):
        musician_types = {
            "Guitarist": Guitarist,
            "Drummer": Drummer,
            "Singer": Singer
        }

        if musician_type not in musician_types:
            raise ValueError("Invalid musician type!")
        current_musician = self.get_musician_by_name(name)

        if current_musician:
            raise Exception(f"{name} is already a musician!")
        # if musician_type == 'Guitarist':
        #     new_musician = Guitarist(name, age)
        #     self.musicians.append(new_musician)
        # elif musician_type == 'Drummer':
        #     new_musician = Drummer(name, age)
        #     self.musicians.append(new_musician)
        # elif musician_type == "Singer":
        #     new_musician = Singer(name, age)
        #     self.musicians.append(new_musician)

        new_musician = musician_types[musician_type](name, age)
        self.musicians.append(new_musician)

        return f"{name} is now a {musician_type}."

    def create_band(self, name: str):
        if self.get_band_by_name(name):
            raise Exception(f"{name} band is already created!")

        new_band = Band(name)
        self.bands.append(new_band)
        return f"{name} was created."

    def create_concert(self, genre: str, audience: int, ticket_price: float, expenses: float, place: str):
        for concert in self.concerts:
            if concert.place == place:
                raise Exception(f"{place} is already registered for {concert.genre} concert!")
        new_concert = Concert(genre, audience, ticket_price, expenses, place)
        self.concerts.append(new_concert)
        return f"{genre} concert in {place} was added."

    def add_musician_to_band(self, musician_name: str, band_name: str):
        musician = self.get_musician_by_name(musician_name)
        if not musician:
            raise Exception(f"{musician_name} isn't a musician!")

        band = self.get_band_by_name(band_name)
        if not band:
            raise Exception(f"{band_name} isn't a band!")

        band.members.append(musician)
        return f"{musician_name} was added to {band_name}."

    def remove_musician_from_band(self, musician_name: str, band_name: str):
        band = self.get_band_by_name(band_name)
        if not band:
            raise Exception(f"{band_name} isn't a band!")

        for musician in band.members:
            if musician.name == musician_name:
                band.members.remove(musician)
                return f"{musician_name} was removed from {band_name}."

        raise Exception(f"{musician_name} isn't a member of {band_name}!")

    def start_concert(self, concert_place: str, band_name: str):
        concert = self.get_concert_by_place(concert_place)
        current_band = self.get_band_by_name(band_name)
        for musician in current_band.members:
            if musician.__class__.__name__ == 'Drummer':
                band_musicians['drummer'] += 1

            elif musician.__class__.__name__ == 'Singer':
                band_musicians['singer'] += 1
            elif musician.__class__.__name__ == 'Guitarist':
                band_musicians['guitarist'] += 1

        for k, v in band_musicians.items():
            if v == 0:
                raise Exception(f"{current_band.name} can't start the concert because it doesn't have enough members!")

        if concert.genre == 'Rock':
            for band_member in current_band.members:
                if band_member.__class__.__name__ == 'Drummer' and \
                         "play the drums with drumsticks" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Singer' and "sing high pitch notes" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Guitarist' and "play rock" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")

        elif concert.genre == 'Metal':
            for band_member in current_band.members:
                if band_member.__class__.__name__ == 'Drummer' and "play the drums with drumsticks" not in \
                        band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Singer' and "sing low pitch notes" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Guitarist' and "play metal" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")

        elif concert.genre == 'Jazz':
            for band_member in current_band.members:
                if band_member.__class__.__name__ == 'Drummer' \
                        and "play the drums with drum brushes" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Singer' \
                        and ("sing low pitch notes" not in band_member.skills
                             or "sing high pitch notes" not in band_member.skills):
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")
                if band_member.__class__.__name__ == 'Guitarist' and "play jazz" not in band_member.skills:
                    raise Exception(f"The {band_name} band is not ready to play at the concert!")

        profit = (concert.audience * concert.ticket_price) - concert.expenses
        return f"{band_name} gained {profit:.2f}$ from the {concert.genre} concert in {concert_place}."
