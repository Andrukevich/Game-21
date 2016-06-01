from random import shuffle

class Card:
    """Description of a current card."""
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def __str__(self):
       return '{}: {}'.format(self.__name, self.__value)

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def set_value(self, number):
        self.__value = number


class Deck:
    """Creation of a deck"""
    __massive_element = ['6', '7', '8', '9', 'Korol', 'Valet', 'Dama', '10', 'Tyz']
    __massive_value = [6, 7, 8, 9, 4, 2, 3, 10, 11]
    __massive_color = ['\u2660', '\u2665', '\u2663', '\u2666']
    def __init__(self):
        self.__array_cards = []
        for i in range(len(self.__class__.__massive_element)):
            for j in range(len(self.__class__.__massive_color)):
                self.__array_cards.append(Card((self.__class__.__massive_element[i] + \
                                                self.__class__.__massive_color[j]), self.__class__.__massive_value[i]))

    def shuffle_deck(self):
        shuffle(self.__array_cards)
        return self.__array_cards

    def add_card(self):
        return self.__array_cards.pop()

    def get_deck(self):
        return self.__array_cards


class Hand:
    """Availability of cards in hand and points"""
    def __init__(self):
        self._current_sum = 0
        self.__array_cards = []
        self.__count_tyz = 0
        self._allow = True

    def __contains__(self, verify):
        for i in  self.__array_cards:
            value = i.get_name()
            if value[0:3] == verify:
                return True
            else:
                continue
        return False

    def add_card_hand(self, take_cards):
        if self._current_sum < 21:
            self.__array_cards.append(take_cards)
            self._current_sum = self.get_sum()
        if  self._current_sum > 21 and 'Tyz' in self:
            for i in self.__array_cards:
                name = i.get_name()
                if name[0:3] == 'Tyz':
                    i.set_value(1)
                    break
            return self.get_sum()

    def get_sum(self):
        self._current_sum = 0
        for i in self.__array_cards:
            self._current_sum += i.get_value()
        return self._current_sum

    def your_cards(self):
        for i in self.__array_cards:
            print (i.get_name())

    def count_tyz(self):
        self.__count_tyz = 0
        for i in self.__array_cards:
            check = i.get_name()
            if check[0:3] == 'Tyz':
                self.__count_tyz += 1
        return self.__count_tyz

    def your_sum(self):
        return self._current_sum


class Player(Hand):
    """Availability of cards at the player and points"""
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

    def your_cards(self):
        print ('Your cards, ', self.__name, ':')
        super().your_cards()

    def get_allow(self):
        if self._current_sum < 21 and self._allow:
            return True
        else:
            return False

    def set_allow(self):
        self._allow = False
        return self._allow


class Bot(Hand):
    """Availability of cards at a computer and points"""
    def __init__(self):
        super().__init__()
        self.__limit = 17

    def your_cards(self):
        print ('Computer cards:')
        super().your_cards()

    def get_allow(self):
        if self._current_sum <= self.__limit:
            return True
        else:
            return False

class Accept:
    """The logic of the game"""
    def __init__(self):
        accept = input('You are playing versus computer.  Cards deal from the end of the deck. Every card gives you \n\
points: Ace – 11, King – 4, Queen – 3, Jack – 2, Ten – 10, Nine – 9, Eight – 8, Seven – 7, Six – 6. The aim of this \n\
game is a getting 21 points at the final stage or a getting score as close as possible to 21. In order to be the \n\
winner you must have more points than your opponent, but your score must be no more than 21. Two cards are available \n\
for each player (you and computer) after the first deal. If you and your opponent don’t have enough points to achieve \n\
21 after the first deal you and your opponent can ask one more card. In this case the next deal starts from you. If \n\
you have Two Aces after the first deal you score 21 automatically. If you get more than 21 but you have the one Ace, \n\
the points of Ace decrease to 1 point (it works one time only). If you have the same points with computer at the end \n\
of the game, your opponent becomes the winner.\nDo you want to play? yes\\no ')
        if accept == 'yes':
            deck = Deck()
            deck.shuffle_deck()
            check_deck = []
            for i in deck.get_deck():
                check_deck.append(i)
            player_name = input('What is your name? ')
            player = Player(player_name)
            bot = Bot()
            for i in range(2):
                player.add_card_hand(deck.add_card())
                bot.add_card_hand(deck.add_card())
            player.your_cards()
            print (player.your_sum(), '\n')
            if player.count_tyz() == 2 or bot.count_tyz() == 2:
                pass
            else:
                while bot.get_allow() or player.get_allow():
                    if player.get_allow() == True:
                        next_card_for_player = input('Take one more card? yes/no ')
                        if next_card_for_player == 'yes':
                            player.add_card_hand(deck.add_card())
                            player.your_cards()
                            print (player.your_sum(), '\n')
                        else:
                            player.set_allow()
                    if bot.get_allow() == True:
                        bot.add_card_hand(deck.add_card())

            if player.your_sum() > 21 and bot.your_sum() > 21:
                print ('\n!!!!!No winner!!!!!\n')
            elif (player.your_sum() <= 21 and player.your_sum() > bot.your_sum()) or \
                    (player.your_sum() <= 21 and bot.your_sum() > 21) or (player.count_tyz() == 2 and bot.your_sum() \
                    != 21):
                print ('\n!!!!!Winner: ', player.get_name(),'!!!!!\n')
            elif (player.count_tyz() == 2 and bot.count_tyz() == 2) or (player.your_sum() == 21 and bot.count_tyz() == \
               2) or (bot.your_sum() and player.count_tyz() == 2) or (player.count_tyz() == 2 and bot.your_sum() == 21):
                print ('\n!!!!!Winner: Computer!!!!!\n')
            else:
                print ('\n!!!!!Winner: Computer!!!!!\n')

            player.your_cards()
            print (player.your_sum(), '\n')
            bot.your_cards()
            print (bot.your_sum(), '\n')
            last_step = input('The game was fair! Do you want check deck? yes/no ')
            if last_step == 'yes':
                for i in check_deck:
                    print (i)

Accept()