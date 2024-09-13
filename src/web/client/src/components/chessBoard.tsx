import React, { useState, useEffect } from "react";
import "./chessBoard.css"; 

type Square = {
  row: number;
  col: number;
  piece: string | null; 
};

type Move = {
  row: number;
  col: number;
};

const initialBoard: Square[][] = [
  [
    { row: 0, col: 0, piece: 'bR' }, { row: 0, col: 1, piece: 'bN' }, { row: 0, col: 2, piece: 'bB' }, { row: 0, col: 3, piece: 'bQ' }, 
    { row: 0, col: 4, piece: 'bK' }, { row: 0, col: 5, piece: 'bB' }, { row: 0, col: 6, piece: 'bN' }, { row: 0, col: 7, piece: 'bR' }
  ],
  Array(8).fill({ piece: 'bP' }).map((p, col) => ({ row: 1, col, piece: p.piece })),
  Array(8).fill({ row: 2, col: 0, piece: null }), 
  Array(8).fill({ row: 3, col: 0, piece: null }),
  Array(8).fill({ row: 4, col: 0, piece: null }),
  Array(8).fill({ row: 5, col: 0, piece: null }),
  Array(8).fill({ piece: 'wP' }).map((p, col) => ({ row: 6, col, piece: p.piece })),
  [
    { row: 7, col: 0, piece: 'wR' }, { row: 7, col: 1, piece: 'wN' }, { row: 7, col: 2, piece: 'wB' }, { row: 7, col: 3, piece: 'wQ' }, 
    { row: 7, col: 4, piece: 'wK' }, { row: 7, col: 5, piece: 'wB' }, { row: 7, col: 6, piece: 'wN' }, { row: 7, col: 7, piece: 'wR' }
  ]
];

const ChessBoard: React.FC = () => {
  const [board, setBoard] = useState<Square[][]>(initialBoard);
  const [selectedPiece, setSelectedPiece] = useState<Square | null>(null);
  const [possibleMoves, setPossibleMoves] = useState<Move[]>([]);

  const handleSquareClick = async (square: Square) => {
    if (selectedPiece && selectedPiece.piece) {
      await makeMove(selectedPiece, square);
      setSelectedPiece(null);
      setPossibleMoves([]);
    } else if (square.piece) {
      setSelectedPiece(square);
      const moves = await fetchPossibleMoves(square);
      setPossibleMoves(moves);
    }
  };

  const fetchPossibleMoves = async (square: Square): Promise<Move[]> => {
    const response = await fetch("/get_possible_moves", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ position: square }),
    });
    const data = await response.json();
    return data.possible_moves; 
  };

  const makeMove = async (from: Square, to: Square) => {
    const response = await fetch("/make_move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        start: { row: from.row, col: from.col },
        end: { row: to.row, col: to.col },
      }),
    });
    const data = await response.json();
    if (data.status === "success") {
      setBoard(updateBoard(from, to));
    }
  };

  const updateBoard = (from: Square, to: Square): Square[][] => {
    const newBoard = [...board];
    newBoard[to.row][to.col] = { ...to, piece: from.piece };
    newBoard[from.row][from.col] = { ...from, piece: null };
    return newBoard;
  };

  return (
    <div className="chess-board">
      {board.map((row, rowIndex) =>
        row.map((square, colIndex) => (
          <div
            key={`${rowIndex}-${colIndex}`}
            className="square"
            onClick={() => handleSquareClick(square)}
            style={{
              backgroundColor: (rowIndex + colIndex) % 2 === 0 ? '#eeeed2' : '#769656', 
            }}
          >
            {square.piece && <div className={`piece ${square.piece}`} />}
          </div>
        ))
      )}
    </div>
  );
};

export default ChessBoard;