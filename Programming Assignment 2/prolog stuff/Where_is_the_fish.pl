/*Here we have different kind of facts: 1)straight forward fact about the house
                                        2)detail regarding the neighbour
			                3)detail regarding the house left to a house
					4)position facts */

/*left_to(X,Y) rule will define the house X positioned left to house Y. */

left_to(X,Y,[X,Y,_,_,_]).
left_to(X,Y,[_,X,Y,_,_]).
left_to(X,Y,[_,_,X,Y,_]).
left_to(X,Y,[_,_,_,X,Y]).

/*neighbour rule which tells that the two houses are neighbours of each other */

neighbour(W,Z,Road):-
	left_to(W,Z,Road);
	left_to(Z,W,Road).

/*Defining a rule find_fish which tells about the problem statement.*/

find_fish(Road,WHO):-
	Road=[ [_,norwegian,_,_,_],
	       [blue,_,_,_,_],
	       [_,_,_,milk,_],_,_
	    /*[Color1,Nation1,Pet1,Drinks1,Smokes1],
	     [Color2,Nation2,Pet2,Drinks2,Smokes2],
	     [Color3,Nation3,Pet3,Drinks3,Smokes3],
	     [Color4,Nation4,Pet4,Drinks4,Smokes4],
	     [Color5,Nation5,Pet5,Drinks5,Smokes5]
	*/
	],

	/*straight forward facts about the house*/
	member([red,english,_,_,_],    Road),
	member([_,swede,dogs,_,_],     Road),
	member([_,dane,_,tea,_],       Road),
	member([green,_,_,coffee,_],   Road),
	member([_,_,birds,_,pallmall], Road),
	member([yellow,_,_,_,dunhills],Road),
	member([_,_,_,bier,bluemaster],Road),
	member([_,german,_,_,prince],  Road),
	member([_,WHO,fish,_,_],       Road),

	/*position facts
	Nation1 = norwegian,
	Drinks3 = milk,
	*/

	/*Neighbourhood facts*/
	neighbour([_,_,_,_,blend],[_,_,cats,_,_],Road),
	neighbour([_,_,horse,_,_],[_,_,_,_,dunhill],Road),
	/*neighbour([_,norwegian,_,_,_],[blue,_,_,_,_],Road), */
	neighbour([_,_,_,_,blend],[_,_,_,water,_],Road),

	/*House to the left*/
	left_to([green,_,_,_,_],[white,_,_,_,_],Road).
















