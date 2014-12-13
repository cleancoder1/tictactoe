current_player = ' ';
state = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']];


function new_game(){
	for (var row=0; row<3; ++row){
		for (var column=0; column<3; ++column){
			set_state(row, column, ' ')
		}
	}
	
	current_player = 'X';
}
	
function set_state(row, column, nstate){
	state[row][column] = nstate
	if (nstate === ' ' || nstate === 'X'){
		$("#O"+row+column).hide();		
	}
	else
	{
		$("#O"+row+column).show();				
	}
	if (nstate === ' ' || nstate === 'O'){
		$("#X"+row+column).hide();		
	}
	else
	{
		$("#X"+row+column).show();				
	}
}

function computer_play(){
	if (current_player !== 'O'){return;}
	
	for (var row=0; row<3; ++row){
		for (var column=0; column<3; ++column){
			if (state[row][column] === ' '){
				set_state(row, column, 'O');
				current_player = 'X';
				check_win()
				return;
			}
		}	
	}
}

function check_win(){
	the_winner = winner();
	if (the_winner === 'X'){
		alert("Congratulations!\nYou Win!")
		current_player = ' '
	}
	if (the_winner === 'O'){
		alert("Game Over!\nYou Lose!")
		current_player = ' '
	}
	if (the_winner === 'tie'){
		alert("Game Over!\nBoring, its a tie.")
		current_player = ' '
	}
}

function winner(){
	for (var i=0; i<3; ++i){
		if (state[i][0] !== ' ' && state[i][0] === state[i][1] && state[i][0] === state[i][2]){
			return state[i][0];
		}
		if (state[0][i] !== ' ' && state[0][i] === state[1][i] && state[0][i] === state[2][i]){
			return state[0][i];
		}
	}
	if (state[1][1] !== ' '){
		if ((state[0][0] === state[1][1] && state[2][2] === state[1][1]) ||
			(state[0][2] === state[1][1] && state[2][0] === state[1][1])){
			return state[1][1];
		}
	}
	for (var row=0; row<3; ++row){
		for (var column=0; column<3; ++column){
			if(state[row][column] === ' ')
				return 'continue';
		}
	}
	return 'tie';
}

function click_square(row, column){
	if (state[row][column] === ' ' && current_player === 'X'){
		current_player = 'O';
		set_state(row, column, 'X');
		check_win()
		setTimeout(computer_play, 300);
	}
}

$("#playfield").click(function(event){
	if (current_player === ' '){
		new_game();
	}
	else if (current_player === 'X'){
		var offset = $(this).offset();
		click_square(Math.floor((event.pageY - offset.top)/200), Math.floor((event.pageX - offset.left)/200));
	}
});