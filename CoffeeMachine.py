class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans=120
        self.cups=9
        self.money=550
    

    def fill_machine(self):
        fill_water= int(input('Write how many ml of water do you want to add:'))
        fill_milk = int(input('Write how many ml of milk do you want to add:'))
        fill_beans = int(input('Write how many grams of coffee beans do you want to add: '))
        fill_cups = int(input('Write how many disposable cups of coffee do you want to add: '))
        self.water += fill_water
        self.milk += fill_milk
        self.beans += fill_beans
        self.cups += fill_cups


    def buy_coffee(self, coffee_type):
        assert coffee_type == '1' or coffee_type == '2' or coffee_type == '3'
        use_water = 0
        use_milk = 0
        use_beans = 0
        use_cups = 0
        add_money = 0
        if coffee_type == '1':
            use_water = 250
            use_beans = 16
            use_cups = 1
            add_money = 4
        elif coffee_type == '2':
            use_water = 350
            use_milk = 75
            use_beans = 20
            use_cups = 1
            add_money = 7
        elif coffee_type == '3':
            use_water = 200
            use_milk = 100
            use_beans = 12
            use_cups = 1
            add_money = 6
        if self.water - use_water < 0:
            print('Sorry, not enough water!')
        elif self.milk - use_milk < 0:
            print('Sorry, not enough milk!')
        elif self.beans - use_beans <0:
            print('Sorry, not enough beans!')
        elif self.cups - use_cups < 0:
            print('Sorry, not enough cups!')
        else:
            print('I have enough resources, making you a coffee!')
            self.water -= use_water
            self.milk -= use_milk
            self.beans -= use_beans
            self.cups -= use_cups
            self.money += add_money

    def take(self):
        print('I gave you $' + str(self.money) )
        self.money=0


    def current_status(self):
        print('The coffee machine has:')
        print(str(self.water) + ' of water')
        print(str(self.milk) + ' of milk')
        print(str(self.beans) + ' of coffee beans')
        print(str(self.cups) + ' of disposable cups')
        print('$' + str(self.money) + ' of money')

coffee_maker = CoffeeMachine()
action = input('\nWrite action (buy, fill, take, remaining, exit):')
while action != 'exit':
    if action == 'buy':
        coffee_type = input('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        if coffee_type == 'back':
            action = input('\nWrite action (buy, fill, take, remaining, exit):')
        else:
            coffee_maker.buy_coffee(coffee_type)
            action = input('\nWrite action (buy, fill, take, remaining, exit):')
    elif action == 'fill':
        coffee_maker.fill_machine()
        action = input('\nWrite action (buy, fill, take, remaining, exit):')
    elif action == 'take':
        coffee_maker.take()
        # current_status(new_water,new_milk,new_beans,new_cups,new_money)
        action = input('\nWrite action (buy, fill, take, remaining, exit):')
    elif action == 'remaining':
        coffee_maker.current_status()
        action = input('\nWrite action (buy, fill, take, remaining, exit):')