// PLEASE ONLY CHANGE THIS FILE WHERE INDICATED.

int n = ...;
int m = ...;

range V = 1..n;
range W = 1..m;

float G[V][V] = ...; //image
float H[W][W] = ...; //shape

// Define here your decision variables and any other auxiliary data.
// You can run an execute block if needed.

int b[u1 in V][u2 in V];
int c[w1 in W][w2 in W];

dvar boolean a[w in W, u in V];   // 1 if node w corresponds with node V

dvar boolean z[w in W, w2 in W, u in V, u2 in V];
dvar float z2[w in W, w2 in W, u in V, u2 in V];

execute timeTermination {
  cplex.tilim = 30*60; //set time model stop (seconds)
}

execute {
  for (var i=1;i<=m;i++) {
  	for (var j=1;j<=m;j++){
  		if (H[i][j] > 0) {
  			c[i][j] = 1;
   }  			
  	}
	}    		
  			
  for (var i=1;i<=n;i++) {
  	for (var j=1;j<=n;j++){
  		if (G[i][j] > 0) {
  			b[i][j] = 1;
   }  			
  }  		
	}  
}

minimize // Write here the objective function.

sum(w, w_ in W: w<w_)(sum(u, u_ in V) (z2[w,w_,u,u_]));


subject to {

    // Write here the constraints.
    forall (u in V)
      sum(w in W) a[w,u] <= 1; //all nodes in image must be taken at least 1
      
    forall (w in W)
      sum(u in V) a[w,u] == 1;  // all nodes in shape must be taken once
      
    forall (u in V, uj in V, w in W, wj in W) { // Isomorphism
      a[w,u] + a[wj,uj] + c[w,wj] - 2 <= b[u,uj] ; 
      a[w,u] + a[wj,uj] + b[u,uj] - 2 <= c[w,wj] ; 
    }      
      
    forall (w in W, wj in W, u in V, uj in V) { //there exists a link between AB and 12
      z[w, wj, u, uj] <= a[w,u]; //
      z[w, wj, u, uj] <= a[wj, uj];
      z[w, wj, u, uj] <= c[w,wj];
      z[w, wj, u, uj] >= a[w,u] + a[wj,uj] + c[w,wj] - 2;
      
      // Absolute value and int*boolean
      z2[w, wj, u, uj] >= (H[w][wj] - G[u][uj])*z[w, wj, u, uj];
      z2[w, wj, u, uj] >= (G[u][uj] - H[w][wj])*z[w, wj, u, uj];
      
   }
        
}


execute {
    
    for (var x in W) {
	var fx = 0;
  	for (var u in V) {
  	    if (a[x][u] == 1) fx = u;
    	}
	writeln("f(" + x + ") = " + fx);
	
    }
    
    for (var x in W) {
      for (var y in W) {
	  	for (var u in V) {
  	      for (var v in V) {
  	        if (a[x][u] == 1 && a[y][v] == 1 && H[x][y] == 0 && G[u][v] > 0) {
  	             writeln("error");
              }
            if (a[x][u] == 1 && a[y][v] == 1 && H[x][y] > 0 && G[u][v] == 0) {
                writeln("error");
  	        }
          }  	         
  	    }
      }
    }
  }   