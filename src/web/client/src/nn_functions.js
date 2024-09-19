const API_URL = process.env.REACT_APP_API_URL;

export async function predictMoves(game_id) {
    if (!game_id) {
        console.error("No game ID available. Cannot get engine move.");
        return;
    }

    // Make the request to get the engine's move
    const response = await fetch(`${API_URL}/engine_move/${game_id}`, {
        method: 'PUT',
    });

    const data = await response.json();
    console.log("Engine move data: ", data);
    // Check if the response status is success
    if (data.status === "success") {
        const engineMove = data.next_move;  // The engine's move in algebraic notation
        //const newFen = data.fen;  // The updated FEN string representing the board state
        
        console.log("Engine move: ", engineMove);
        //console.log("Updated board state (FEN): ", newFen);

        // Update the board with the new move
        //chess.load(newFen);  // Load the new FEN state into the chess.js game
        //board.setPosition(newFen, true);  // Set the board position based on FEN
        //make_move(engineMove);  // Make the move on the board

        return engineMove;  // Return the move if needed for further processing
    } else {
        console.error("Error fetching engine move: ", data);
        return null;
    }
}
