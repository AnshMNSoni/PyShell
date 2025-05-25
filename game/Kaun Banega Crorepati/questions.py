# questions.py - Contains all questions for the KBC game

def get_questions():
    """
    Returns a list of all questions for the KBC game.
    Each question is a dictionary with keys:
    - question: The question text
    - options: List of 4 options
    - correct: The correct answer (must match one of the options exactly)
    - value: The dollar value of the question
    - hint: A hint for the question
    - penalty: Optional penalty for wrong answer (only for higher questions)
    """
    return [
        # Original questions
        {
            "question": "What is the capital city of France?",
            "options": ["Berlin", "London", "Paris", "Madrid"],
            "correct": "Paris",
            "value": 1000,
            "hint": "Where is eiffel tower located?"
        },
        {
            "question": "Which planet is known as the 'Red Planet'?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "correct": "Mars",
            "value": 2000,
            "hint": "It is the fourth planet from the sun in our solar system!"
        },
        {
            "question": "In which year did the Titanic sink?",
            "options": ["1905", "1912", "1920", "1931"],
            "correct": "1912",
            "value": 3000,
            "hint": "Republic Year of China!"
        },
        {
            "question": "Who wrote the play 'Romeo and Juliet'?",
            "options": ["William Wordsworth", "Charles Dickens", "William Shakespeare", "Jane Austen"],
            "correct": "William Shakespeare",
            "value": 4000,
            "hint": "Often referred as the 'Bard of Avon'"
        },
        {
            "question": "Which element has the chemical symbol 'W'?",
            "options": ["Tungsten", "Vanedium", "Rutherfodium", "Antimony"],
            "correct": "Tungsten",
            "value": 5000,
            "hint": "This element is known for its exceptional hardness and high melting point"
        },
        {
            "question": "Name of Raja Dashratha's Mother is?",
            "options": ["Rupwati", "Indumati", "Sumitra", "Kaushaliya"],
            "correct": "Indumati",
            "value": 6000,
            "penalty": 1000,
            "hint": "Sanskrit word associated with purity and beauty"
        },
        {
            "question": "How many verses are there in 'Bhagavad Geeta'?",
            "options": ["520", "600", "910", "700"],
            "correct": "700",
            "value": 7000,
            "penalty": 2000,
            "hint": "It is divisible by 100"
        },
        
        # Additional questions - General Knowledge
        {
            "question": "Which country is known as the Land of the Rising Sun?",
            "options": ["China", "Thailand", "Japan", "South Korea"],
            "correct": "Japan",
            "value": 1000,
            "hint": "This country's flag features a red circle on a white background"
        },
        {
            "question": "What is the largest ocean on Earth?",
            "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
            "correct": "Pacific Ocean",
            "value": 2000,
            "hint": "It covers more than 30% of the Earth's surface"
        },
        {
            "question": "Which is the smallest prime number?",
            "options": ["0", "1", "2", "3"],
            "correct": "2",
            "value": 1000,
            "hint": "It's the only even prime number"
        },
        {
            "question": "Who painted the Mona Lisa?",
            "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
            "correct": "Leonardo da Vinci",
            "value": 3000,
            "hint": "He was also a scientist and inventor from Italy"
        },
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "correct": "Au",
            "value": 2000,
            "hint": "It comes from the Latin word 'aurum'"
        },
        
        # Science and Technology
        {
            "question": "What is the hardest natural substance on Earth?",
            "options": ["Platinum", "Diamond", "Titanium", "Quartz"],
            "correct": "Diamond",
            "value": 3000,
            "hint": "It's made of carbon atoms arranged in a crystal structure"
        },
        {
            "question": "Which scientist proposed the theory of relativity?",
            "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Galileo Galilei"],
            "correct": "Albert Einstein",
            "value": 4000,
            "hint": "He developed the formula E=mc²"
        },
        {
            "question": "What is the main component of the Sun?",
            "options": ["Oxygen", "Carbon", "Helium", "Hydrogen"],
            "correct": "Hydrogen",
            "value": 4000,
            "hint": "It's the lightest and most abundant element in the universe"
        },
        {
            "question": "Which programming language was developed by Guido van Rossum?",
            "options": ["Java", "C++", "Python", "Ruby"],
            "correct": "Python",
            "value": 5000,
            "hint": "It's named after a British comedy group, not the snake"
        },
        {
            "question": "What does CPU stand for?",
            "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Central Processor Utility"],
            "correct": "Central Processing Unit",
            "value": 1000,
            "hint": "It's often called the brain of the computer"
        },
        
        # History
        {
            "question": "Who was the first President of the United States?",
            "options": ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"],
            "correct": "George Washington",
            "value": 2000,
            "hint": "His face appears on the one-dollar bill"
        },
        {
            "question": "In which year did World War II end?",
            "options": ["1943", "1945", "1947", "1950"],
            "correct": "1945",
            "value": 3000,
            "hint": "Japan surrendered after atomic bombs were dropped on Hiroshima and Nagasaki"
        },
        {
            "question": "Which ancient civilization built the Machu Picchu?",
            "options": ["Aztecs", "Mayans", "Incas", "Olmecs"],
            "correct": "Incas",
            "value": 5000,
            "hint": "This civilization was based in Peru"
        },
        {
            "question": "Who wrote the 'Origin of Species'?",
            "options": ["Isaac Newton", "Charles Darwin", "Albert Einstein", "Galileo Galilei"],
            "correct": "Charles Darwin",
            "value": 4000,
            "hint": "He developed the theory of evolution by natural selection"
        },
        {
            "question": "Which empire was ruled by Genghis Khan?",
            "options": ["Roman Empire", "Ottoman Empire", "Mongol Empire", "Byzantine Empire"],
            "correct": "Mongol Empire",
            "value": 6000,
            "penalty": 1000,
            "hint": "It was the largest contiguous land empire in history"
        },
        
        # Geography
        {
            "question": "What is the capital of Australia?",
            "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
            "correct": "Canberra",
            "value": 3000,
            "hint": "It's not the largest city in the country"
        },
        {
            "question": "Which is the longest river in the world?",
            "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
            "correct": "Nile",
            "value": 4000,
            "hint": "It flows through 11 countries in northeastern Africa"
        },
        {
            "question": "Which country is known as the Land of Fire and Ice?",
            "options": ["Norway", "Canada", "Iceland", "Russia"],
            "correct": "Iceland",
            "value": 5000,
            "hint": "It has both volcanoes and glaciers"
        },
        {
            "question": "What is the smallest country in the world?",
            "options": ["Monaco", "Nauru", "Vatican City", "San Marino"],
            "correct": "Vatican City",
            "value": 3000,
            "hint": "It's an independent state located within Rome, Italy"
        },
        {
            "question": "Which mountain range separates Europe from Asia?",
            "options": ["Alps", "Himalayas", "Andes", "Ural Mountains"],
            "correct": "Ural Mountains",
            "value": 6000,
            "penalty": 1000,
            "hint": "They run north to south through Russia"
        },
        
        # Sports
        {
            "question": "In which sport would you perform a slam dunk?",
            "options": ["Volleyball", "Basketball", "Tennis", "Football"],
            "correct": "Basketball",
            "value": 1000,
            "hint": "It involves putting the ball directly through the hoop with one or both hands"
        },
        {
            "question": "Which country won the FIFA World Cup in 2018?",
            "options": ["Brazil", "Germany", "Argentina", "France"],
            "correct": "France",
            "value": 2000,
            "hint": "Their national team is known as 'Les Bleus'"
        },
        {
            "question": "How many players are there in a standard cricket team?",
            "options": ["9", "10", "11", "12"],
            "correct": "11",
            "value": 3000,
            "hint": "The same number as in a soccer team"
        },
        {
            "question": "Which tennis player has won the most Grand Slam titles in men's singles?",
            "options": ["Roger Federer", "Rafael Nadal", "Novak Djokovic", "Pete Sampras"],
            "correct": "Novak Djokovic",
            "value": 5000,
            "hint": "He's from Serbia"
        },
        {
            "question": "In which city were the first modern Olympic Games held in 1896?",
            "options": ["Paris", "Athens", "London", "Rome"],
            "correct": "Athens",
            "value": 4000,
            "hint": "The Games returned to this city in 2004"
        },
        
        # Entertainment
        {
            "question": "Who played the character of Harry Potter in the movie series?",
            "options": ["Rupert Grint", "Daniel Radcliffe", "Tom Felton", "Emma Watson"],
            "correct": "Daniel Radcliffe",
            "value": 1000,
            "hint": "He was just 11 years old when cast for the first movie"
        },
        {
            "question": "Which band performed the hit song 'Bohemian Rhapsody'?",
            "options": ["The Beatles", "Led Zeppelin", "Queen", "Pink Floyd"],
            "correct": "Queen",
            "value": 2000,
            "hint": "Their lead singer was Freddie Mercury"
        },
        {
            "question": "Who is known as the 'King of Pop'?",
            "options": ["Elvis Presley", "Michael Jackson", "Prince", "David Bowie"],
            "correct": "Michael Jackson",
            "value": 3000,
            "hint": "He released the best-selling album 'Thriller'"
        },
        {
            "question": "Which movie won the Best Picture Oscar in 2020?",
            "options": ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"],
            "correct": "Parasite",
            "value": 4000,
            "hint": "It was the first non-English language film to win this award"
        },
        {
            "question": "Who wrote the 'Harry Potter' book series?",
            "options": ["J.R.R. Tolkien", "J.K. Rowling", "George R.R. Martin", "Suzanne Collins"],
            "correct": "J.K. Rowling",
            "value": 2000,
            "hint": "She initially used her initials to appeal to male readers"
        },
        
        # Indian Culture and History
        {
            "question": "Who was the first Prime Minister of India?",
            "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Rajendra Prasad"],
            "correct": "Jawaharlal Nehru",
            "value": 2000,
            "hint": "He served from 1947 until his death in 1964"
        },
        {
            "question": "Which festival is known as the 'Festival of Lights' in India?",
            "options": ["Holi", "Diwali", "Navratri", "Durga Puja"],
            "correct": "Diwali",
            "value": 1000,
            "hint": "People light oil lamps and candles during this festival"
        },
        {
            "question": "Which Indian classical dance form originated in Tamil Nadu?",
            "options": ["Kathak", "Bharatanatyam", "Odissi", "Kuchipudi"],
            "correct": "Bharatanatyam",
            "value": 4000,
            "hint": "It's one of the oldest classical dance forms in India"
        },
        {
            "question": "Who wrote the Indian national anthem 'Jana Gana Mana'?",
            "options": ["Rabindranath Tagore", "Bankim Chandra Chattopadhyay", "Sarojini Naidu", "Mahatma Gandhi"],
            "correct": "Rabindranath Tagore",
            "value": 3000,
            "hint": "He was the first non-European to win the Nobel Prize in Literature"
        },
        {
            "question": "In which year did India gain independence from British rule?",
            "options": ["1945", "1947", "1950", "1952"],
            "correct": "1947",
            "value": 2000,
            "hint": "Independence was achieved on August 15th"
        },
        
        # Difficult Questions (with penalties)
        {
            "question": "What is the only letter that doesn't appear in any U.S. state name?",
            "options": ["Q", "X", "Z", "J"],
            "correct": "Q",
            "value": 6000,
            "penalty": 1000,
            "hint": "It's one of the least commonly used letters in English"
        },
        {
            "question": "Which element was discovered by Marie Curie?",
            "options": ["Radium", "Uranium", "Plutonium", "Nobelium"],
            "correct": "Radium",
            "value": 6000,
            "penalty": 1000,
            "hint": "She named it after the Latin word for 'ray'"
        },
        {
            "question": "What is the world's most expensive spice by weight?",
            "options": ["Vanilla", "Cardamom", "Saffron", "Cinnamon"],
            "correct": "Saffron",
            "value": 6000,
            "penalty": 1000,
            "hint": "It comes from a type of crocus flower"
        },
        {
            "question": "Which philosopher said 'I think, therefore I am'?",
            "options": ["Socrates", "René Descartes", "Plato", "Aristotle"],
            "correct": "René Descartes",
            "value": 7000,
            "penalty": 2000,
            "hint": "He was a French philosopher, mathematician, and scientist"
        },
        {
            "question": "What is the smallest bone in the human body?",
            "options": ["Stapes", "Femur", "Radius", "Phalanges"],
            "correct": "Stapes",
            "value": 7000,
            "penalty": 2000,
            "hint": "It's located in the middle ear"
        },
        {
            "question": "Which ancient wonder was located in Alexandria?",
            "options": ["Hanging Gardens", "Colossus of Rhodes", "Lighthouse of Alexandria", "Temple of Artemis"],
            "correct": "Lighthouse of Alexandria",
            "value": 7000,
            "penalty": 2000,
            "hint": "It was one of the tallest structures of the ancient world"
        },
        {
            "question": "What is the rarest blood type in humans?",
            "options": ["AB negative", "B negative", "O negative", "A negative"],
            "correct": "AB negative",
            "value": 7000,
            "penalty": 2000,
            "hint": "Less than 1% of the world's population has this blood type"
        }
    ]