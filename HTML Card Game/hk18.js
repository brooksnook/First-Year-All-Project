// stores the last card to be flipped, the number of clicks, and number of pairs
let last_card = 0
let number_of_clicks = 0
let number_of_pairs = 0

// increments clicks
const incrementClicks = () => {
   number_of_clicks++;
   document.querySelector("#clicks").innerHTML = `Clicks : ${number_of_clicks}`;
}

// increments pairs
const incrementPairs = () => {
   number_of_pairs++;
   document.querySelector('#pairs').innerHTML = `Pairs: ${number_of_pairs}`;
}

// creates an array full of objects representing each card
// some help from copilot
const cardObjectsArray = (numbers, suits) => {
   const cards = [];
   let card_number = 0;;
   for(let i = 0; i < numbers.length; i++) {
      for(let j = 0; j < suits.length; j++) {
         card_number += 1;
         let card = {
            number: numbers[i], 
            suit: suits[j], 
            image: `images/${suits[j]}_${numbers[i]}.png`, 
            card_number: card_number,
            alttext: `Card number ${card_number}. ${numbers[i]} of ${suits[j]}s.`
         }
         cards.push(card);
      }
   }
   return cards
}

// flips the card to the front
const flipCardFront = (card) => {
   const img = card.querySelector('img');
   img.src = `images/${card.dataset.suit}_${card.dataset.value}.png`;
   img.alt = `Card number ${card.dataset.card_number}. ${card.dataset.value} of ${card.dataset.suit}s`;
   card.dataset.flipped = 'false'
}

// flips the card to the back
const flipCardBack = (card) => {
   const img = card.querySelector('img');
   img.src = 'images/back.jpg';
   img.alt = `Back of card ${card.dataset.card_number}`;
   card.dataset.flipped = 'true';
}

// flips card
const flipCard = (card) => {
   if(card.dataset.flipped === 'true') {
      flipCardFront(card);
   } else {
      flipCardBack(card);
   }
}


// creates all the cards in the board
const createCards = () => {
   const cardData = cardObjectsArray(['Ace', 2, 3, 4, 5, 6], ['club', 'diamond', 'heart', 'spade']);
   const template = document.querySelector('template');
   const section = document.querySelector('section');
   const size = parseInt(document.querySelector('input[type="radio"][name="board-size"]:checked').value);
   section.innerHTML = '';
   for (let i = 0; i < size; i++) {
      const selectedCard = cardData[i] ;
      const card = template.content.cloneNode(true);
      card.querySelector('.card').dataset.value = selectedCard.number;
      card.querySelector('.card').dataset.suit = selectedCard.suit;
      card.querySelector('.card').dataset.card_number = selectedCard.card_number;
      card.querySelector('.card').dataset.flipped = 'false';
      card.querySelector('img').src = selectedCard.image;
      card.querySelector('img').alt = selectedCard.alttext;
      section.append(card);
   }

   // adds an event listener for flipping the cards over
   document.querySelectorAll(".card").forEach(card => {
      card.addEventListener('click', function() {
         if(card.dataset.flipped === 'true') {
            if(last_card != 0 && last_card.dataset.value === card.dataset.value) {
               flipCard(card);
               last_card.querySelector("img").style.outline = "2px solid yellow";
               card.querySelector("img").style.border = "2px solid yellow";
               incrementPairs();
               last_card = 0;
            } else if (last_card === 0) {
               flipCard(card);
               last_card = card;
            } else {
               flipCard(last_card);
               last_card = 0;
            }

            incrementClicks();

            if(number_of_clicks > (size * 2)) {
               document.querySelector("#lose").showModal();
            } else if (number_of_pairs === (size / 2)) {;
               document.querySelector("#win").showModal();
            };
         }
      })
   });

   // resets last card, clicks, and number of pairs
   last_card = 0;
   number_of_clicks = 0;
   number_of_pairs = 0;
   cardsJustShuffled = false;
   document.querySelector('#pairs').innerHTML = `Pairs: ${number_of_pairs}`;
   document.querySelector('#clicks').innerHTML = `Clicks: ${number_of_clicks}`;
}

// shuffles the cards
// lecturer's code
const getShuffled = (cards) => {
   const list = Array.from(cards);
   for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = list[i];
      list[i] = list[j];
      list[j] = temp;
   }
   return list;
}

window.onload = () => {
   const btnFlip = document.querySelector('#btnFlip');
   const btnShuffle = document.querySelector('#btnShuffle');
   let cardsJustShuffled = false;

   createCards();

   // radio button for selecting the board size
   const board_radio = document.querySelectorAll('input[type="radio"][name="board-size"]');
   board_radio.forEach(radio => {
      radio.addEventListener('change', function() {
         if (this.checked) {
            createCards();
         }
      });
   });

   // shuffles the cards
   btnShuffle.addEventListener('click', () => {
      const section = document.querySelector('section');
      const cards = section.querySelectorAll('.card');
      section.innerHTML = '';
      // shuffle and then update each card's position number
      // some help from copilot
      getShuffled(cards).forEach((card, idx) => {
         const newCardNumber = idx + 1;
         card.dataset.card_number = newCardNumber;
         const img = card.querySelector('img');
         img.alt = `Card number ${newCardNumber}. ${card.dataset.value} of ${card.dataset.suit}s`;
         section.appendChild(card);
      });
      cardsJustShuffled = true
   })

   // for flipping the cards over to the back
   btnFlip.addEventListener('click', () => {
      if (cardsJustShuffled) {
         const cards = document.querySelectorAll('.card')
         cards.forEach((card) => {
            flipCard(card);
         })
         cardsJustShuffled = false;
      } else {
         alert('Please shuffle the cards.');
      }
      document.querySelector("#options-and-buttons").style.display = "none";
   })

   document.querySelectorAll(".play-again").forEach(button => {
      button.addEventListener('click', () => {
         location.reload();
      })
   })
}