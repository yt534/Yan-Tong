#!/usr/bin/env python
# coding: utf-8

# To get data returned by SELECT query you can use fetchone(), fetchall() methods:

# In[1]:


import sqlite3
import random

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute('''DROP TABLE card;''')
cur.execute('''
CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);
''')
conn.commit()

############################# account page #############################

def main_page():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    customer_choice = input()
    if customer_choice == '1':
        global new_cardnum, new_cardpin
        new_cardnum, new_cardpin, balance = cardnum_pin_gen()
        save_to_db(new_cardnum, new_cardpin, balance)
        main_page()
    elif customer_choice == '2':
        log_into()
    elif customer_choice == '0':
        print('\nBye!')


        
def cardnum_pin_gen():
    iin = 400000
    customer_accnum = random.randint(100000000, 999999999)
    check_num = random.randint(0, 9)
    new_cardnum = str(iin) + str(customer_accnum) + str(check_num)
    new_cardpin = str(random.randint(1000, 9999))

    # Luhn algorithm to verify the cardnum
    if luhn(new_cardnum) == True:
        print('\nYour card has been created')
        print('Your card number:')
        print(new_cardnum)
        print('Your card PIN:')
        print(new_cardpin)
        print('')
    elif luhn(new_cardnum) == False:
        new_cardnum, new_cardpin, balance = cardnum_pin_gen()
    balance = 0
    return new_cardnum, new_cardpin, balance



def luhn(cardnum):
    '''
    input: cardnum
    output: Logic expression of whether the cardnum is valid or not
    '''
    drop_last_digit = cardnum[:-1]

    multiply_odd_digits_by2 = []
    for i in range(len(drop_last_digit)):
        if i % 2 == 1:
            multiply_odd_digits_by2.append(int(drop_last_digit[i]))
        else:
            multiply_odd_digits_by2.append(int(drop_last_digit[i])*2)

    subtract9_to_num_over9 = []
    for i in multiply_odd_digits_by2:
        if i>9:
            subtract9_to_num_over9.append(i - 9)
        else:
            subtract9_to_num_over9.append(i)

    add_all_num = 0
    for i in subtract9_to_num_over9:
        add_all_num += i
    add_all_num += int(cardnum[-1])

    if add_all_num%10 == 0:
        return True
    else:
        return False


    
def log_into():
    card_num = input('Enter your card number:')
    card_pin = input('Enter your PIN:')

    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin +'''
                ''')
    result = cur.fetchall()
    count = len(result)
    conn.commit()
    if count != 1:
        print('')
        print('Wrong card number or PIN!')
        print('')
        main_page()
    else:
        print('')
        print('You have successfully logged in!')
        print('')
        account_page(card_num, card_pin)
        return card_num, card_pin
   

    
############################# account page #############################

def account_page(card_num, card_pin):
    print('\n1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')
    customer_choice = input()
    if customer_choice == '1':
        check_balance(card_num, card_pin)
        account_page(card_num, card_pin)
    elif customer_choice == '2':
        add_income(card_num, card_pin)
        account_page(card_num, card_pin)
    elif customer_choice == '3':
        transfer(card_num, card_pin)
        account_page(card_num, card_pin)
    elif customer_choice == '4':
        close_acc(card_num, card_pin)
    elif customer_choice == '5':
        print('\nYou have successfully logged out!\n')
        main_page()
    elif customer_choice == '0':
        print('\nBye!')
        exit()

        

def check_balance(card_num, card_pin):
    cur.execute('''
            SELECT * FROM card 
            WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin)
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
    print('\nBalance: ' + str(balance))
    return balance
        
        

def add_income(card_num, card_pin):
    income = int(input('\nEnter income:'))
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
    new_balance = income + balance
    cur.execute('''
            UPDATE card 
            SET balance = ''' + str(new_balance) + '''
            WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    conn.commit()
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
    print('\nIncome was added!')



def transfer(card_num, card_pin):    
    # check current balance
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
        
    print('\nTransfer')
    card_num_receiver = input('Enter card number:')
    
    # check if card_num_receiver exists
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num_receiver +'''
                ''')
    result = cur.fetchall()
    count = len(result)


    if luhn(card_num_receiver) == False:
        print('\nProbably you made a mistake in the card number. Please try again!')
        account_page(card_num, card_pin)
    elif count != 1:
        print('\nSuch a card does not exist.')
        account_page(card_num, card_pin)
    elif card_num == card_num_receiver:
        print('\nYou can\'t transfer money to the same account!')
        account_page(card_num, card_pin)
    else:
        transfer_amt = int(input('Enter how much money you want to transfer:'))
        if transfer_amt > balance:
            print('Not enough money!')
            account_page(card_num, card_pin)
        else:
            new_balance = balance - transfer_amt
            cur.execute('''
                SELECT balance FROM card 
                WHERE number = ''' + card_num_receiver + '''''')
            result = cur.fetchall()
            balance_receiver = result[0][0]
            conn.commit()
            new_balance_receiver = balance_receiver + transfer_amt
            cur.execute('''
                    UPDATE card 
                    SET balance = ''' + str(new_balance) + '''
                    WHERE number = ''' + card_num + '''''')
            conn.commit()            
            cur.execute('''
                    UPDATE card 
                    SET balance = ''' + str(new_balance_receiver) + '''
                    WHERE number = ''' + card_num_receiver + '''''')
            conn.commit() 
            print('\nSuccess!')
            account_page(card_num, card_pin)
        


def close_acc(card_num, card_pin):
    cur.execute('''
                    DELETE FROM card 
                    WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    conn.commit() 
    print('\nThe account has been closed!')
    main_page()

    
    
def save_to_db(new_cardnum, new_cardpin, balance):
    cur.execute('''
        INSERT INTO card (id, number, pin, balance) 
        VALUES (((select count(*) from card) + 1), ''' + new_cardnum + ''', ''' + new_cardpin + ''', ''' + str(balance) + ''')
                ''')
    conn.commit()   

    


# main program starts here
main_page()


# In[6]:


cur.execute('''
INSERT INTO card (id, number, pin, balance) VALUES (
    22,
    '33321',
    '7732432',
    5)
''')
conn.commit()
cur.execute('''
SELECT * FROM card;
''')
result = cur.fetchall()
for i in result:
    print(i)
#     print
(type(i[0]))


# In[ ]:


card_num = '4000006553582809'
card_pin = '8001'
def add_income(card_num, card_pin):
    income = int(input('Enter income:'))
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
    new_balance = income + balance
    print(new_balance)
    cur.execute('''
            UPDATE card 
            SET balance = ''' + str(new_balance) + '''
            WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    conn.commit()
    cur.execute('''
        SELECT * FROM card 
        WHERE number = ''' + card_num + ''' AND pin = ''' + card_pin + '''''')
    result = cur.fetchall()
    balance = result[0][3]
    conn.commit()
    print(balance)
    print('Income was added!')
    
    
    
add_income(card_num, card_pin)


# In[7]:


luhn('4000003972196502')
# cardnum = '3000003972196503'


# In[ ]:




