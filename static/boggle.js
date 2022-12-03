"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start: Gets a new game and gameId from the API and displays board */

async function start() {
  let response = await axios.post("/api/new-game"); // {"gameId": game_id, "board": game.board}
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board: Displays the game board for the given game
 * 
 * board: array
 * 
 */

function displayBoard(board) {
  $table.empty();
  const $tbody = $('<tbody>');
  for (let i = 0; i < board.length; i++) {

    const $tr = $('<tr>');
    for (let j = 0; j < board.length; j++) {

      $tr.append($('<td>').text(`${board[i][j]}`));
    }

    $tbody.append($tr)
  }

  $table.append($tbody);
}

/** displayMessage: Displays message associated with validity of word
 * 
 * msg: string
 */

function displayMessage(msg) {
  $message.text(msg);
}

/** addValidWordToDOMList: Adds successful word to a bulleted list on the DOM 
 * 
 * word: string
*/

function addValidWordToDOMList(word) {
  $playedWords.append(`<li>${word}</li>`);
}

/** validateWord: Checks if the word is a valid word and on the board. If so, adds
 * it to the list of successful words and displays a relevant message. Otherwise, displays
 * invalidity message
 * 
 * word: string
 */

async function validateWord(word) {
  // let game_id = gameId; // This is a weird fix we had to do and I'm not sure I could explain why
  const response = await axios({
    url: '/api/score-word',
    method: 'POST',
    data: { gameId, word }
  })

  const result = response.data.result

  if (result === 'not-on-board') {
    displayMessage('Word not on board');
  } else if (result === 'not-word') {
    displayMessage('Invalid word (not a word)');
  } else {
    addValidWordToDOMList(word);
    displayMessage(`Added: ${word}`);
  }
}

/** handleWordSubmission: listens for a word submission and validates the word */

async function handleWordSubmission(evt) {
  evt.preventDefault();

  const word = $wordInput.val().toUpperCase();
  $wordInput.val('');

  await validateWord(word);
}


start();

$form.on('submit', handleWordSubmission);