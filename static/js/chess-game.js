document.addEventListener('DOMContentLoaded', function() {
    console.log('Chess script loaded');
    
    let board = null;

    let game = new Chess();
    let $status = $('#status');
    let engine = null;
    let engineStatus = {};

    // Initialize Stockfish engine
    engine = new Worker('/static/js/stockfish.js');
    engine.onmessage = function(event) {
        const line = event.data;
        console.log(`Engine output: ${line}`);

        if (line.startsWith('bestmove')) {
            const bestMove = line.split(' ')[1];
            game.move(bestMove, { sloppy: true });
            board.position(game.fen());
            updateStatus();
        }
    };

    function startEngine() {
        engineStatus.engineReady = false;
        engine.postMessage('uci');
    }

    function makeEngineMove() {
        const difficulty = parseInt($('#difficulty').val());
        engine.postMessage(`setoption name Skill Level value ${difficulty}`);
        engine.postMessage(`position fen ${game.fen()}`);
        engine.postMessage('go');
    }

    function onDragStart(source, piece, position, orientation) {
        // Only pick up pieces for White
        if (game.game_over()) return false;
        if (piece.search(/^b/) !== -1) return false;
    }

    function onDrop(source, target) {
        // See if the move is legal
        const move = game.move({
            from: source,
            to: target,
            promotion: 'q' // Always promote to a queen for example simplicity
        });

        // Illegal move
        if (move === null) return 'snapback';

        updateStatus();
        
        // Make the engine move after a short delay
        window.setTimeout(makeEngineMove, 250);
    }

    function onSnapEnd() {
        board.position(game.fen());
    }

    function updateStatus() {
        let status = '';

        if (game.in_checkmate()) {
            status = 'Game over, ' + (game.turn() === 'w' ? 'black' : 'white') + ' wins!';
        } else if (game.in_draw()) {
            status = 'Game over, drawn position';
        } else {
            status = (game.turn() === 'w' ? 'White' : 'Black') + ' to move';
            if (game.in_check()) {
                status += ', ' + (game.turn() === 'w' ? 'White' : 'Black') + ' is in check';
            }
        }

        $status.html(status);
    }

    const config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        pieceTheme: 'https://chessboardjs.com/img/chesspieces/alpha/{piece}.png'
        // pieceTheme: '/static/img/chesspieces/wikipedia/{piece}.png'


    };

    board = Chessboard('myBoard', config);
    updateStatus();
    startEngine();

    // Buttons
    $('#startBtn').on('click', function() {
        game.reset();
        board.start();
        updateStatus();
        startEngine();
    });

    $('#undoBtn').on('click', function() {
        game.undo();
        game.undo();
        board.position(game.fen());
        updateStatus();
    });

    $('#flipBtn').on('click', board.flip);

    $('#difficulty').on('change', function() {
        startEngine();
    });
});