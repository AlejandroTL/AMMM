/*********************************************
 * OPL 20.1.0.0 Model
 * Author: andre
 * Creation Date: 22 de out de 2021 at 15:46:54
 *********************************************/
// PLEASE ONLY CHANGE THIS FILE WHERE INDICATED.

int n = ...;
int m = ...;

range V = 1..n;
range W = 1..m;

float G[V][V] = ...; //image
float H[W][W] = ...; //shape

// Define here your decision variables and any other auxiliary data.
// You can run an execute block if needed.

// Variable calculated in the "execute".
//  if (G[i][j] > 0) G_edges[i][j] = 1
int G_edges[V][V];
// Variable calculated in the "execute".
//  if (H[i][j] > 0) H_edges[i][j] = 1
int H_edges[W][W];

// Decision variable: 
// If Link[w][v] == 1: 
// 		node v from G correspond to node w from H
dvar boolean Link[W][V];
// Decision variable: 
// If Has_link[w1][w2][v1][v2] == 1: 
// 		Link[w1][v1] > 0 && Link[w2][v2] > 0
dvar boolean Has_link[W][W][V][V];
// Decision variable:
//    Stores the absolute value of H[w1][w2] - G[v1][v2] for all combinations of w1,w2,v1,v2
dvar float Absolute[W][W][V][V];

float temp;
float detTime;
float runTime;

execute{
	var before = new Date();
	temp = before.getTime();
}

execute {
	for (var i=1;i<=m;i++) {
		for (var j=1;j<=m;j++){
			if (H[i][j] > 0) {
				H_edges[i][j] = 1;
			}
		}
	}	
	for (var i=1;i<=n;i++) {
		for (var j=1;j<=n;j++){
			if (G[i][j] > 0) {
				G_edges[i][j] = 1;
			}
		}
	}	
	  
}

minimize // Write here the objective function.
// Summing all values of the Absolute variable that has the absolute difference between all terms from H to all terms of G
// Multiplied by the variable Has_link that is a boolean with 1 if the Link between the edge of G and H is done
// This way, only sums the values that are linked.
// Diveded by 2, once the matrices are symmetric so we are summing twice each error.
sum(w1 in W, w2 in W)
	(sum(v1 in V, v2 in V) 
		(Absolute[w1][w2][v1][v2])*0.5);

subject to {

    // Write here the constraints.
    
    // Contraint 1: 
    // Each Node of G is related to at most a node of H
    forall (v in V)
      sum(w in W) Link[w][v] <= 1;
    // Contraint 2: 
    // Each Node of H is related to exactlly one node of G
    forall (w in W)
      sum(v in V) Link[w][v] == 1;     
    forall (w1 in W, w2 in W, v1 in V, v2 in V) {
    // Contraint 3: 
    // it can only be Link[w1][v1] == 1 && Link[w2][v2] == 1
    // if H_edges[w1][w2] == 1 && G_edges[v1][v2] == 1
      Link[w1][v1] + Link[w2][v2] + H_edges[w1][w2] - 2 <= G_edges[v1][v2] ; 
      Link[w1][v1] + Link[w2][v2] + G_edges[v1][v2] - 2 <= H_edges[w1][w2] ; 
    // Contraint 4: 
    //	if Link[w1][v1] == 1 && Link[w2][v2] == 1
    //	then Has_link[w1][w2][v1][v2] == 1
      Has_link[w1][w2][v1][v2] <= Link[w1][v1];
      Has_link[w1][w2][v1][v2] <= Link[w2][v2];
      Has_link[w1][w2][v1][v2] >= Link[w1][v1] + Link[w2][v2] - 1;
    // Contraint 5: 
    //	Absolute[w1][w2][v1][v2] = absolute_value_of(H[w1][w2] - G[v1][v2])
      Absolute[w1][w2][v1][v2] >= (H[w1][w2] - G[v1][v2])*Has_link[w1][w2][v1][v2];
      Absolute[w1][w2][v1][v2] >= (G[v1][v2] - H[w1][w2])*Has_link[w1][w2][v1][v2];
   }
}

execute{
	var after = new Date();
	runTime = after.getTime()-temp;
	detTime = cplex.getDetTime()
	writeln("solving time ~= ",runTime);
	writeln("Derteministic time ~= ",detTime);
}

execute {
    
    for (var w in W) {
		var fw = 0;
	  	for (var v in V) {
	  	    if (Link[w][v] == 1) fw = v;
	    	}
		writeln("f(" + w + ") = " + fw);
    }

    // Error Checking
    for (var w1 in W) {
      for (var w2 in W) {
	  	for (var v1 in V) {
  	      for (var v2 in V) {
  	        if (Link[w1][v1] == 1 && Link[w2][v2] == 1 && H[w1][w2] == 0 && G[v1][v2] > 0) {
  	             writeln("error");
              }
          }  	         
  	    }
      }
    }
  }  