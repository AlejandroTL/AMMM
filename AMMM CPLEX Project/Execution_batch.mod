main {
  writeln("n, m, c, d, e, cost, time, det_time")
  
    var c=0.3;
    for (var s=40; s<=50; s=s+2) {
	for (var d=0.6;d<=0.6;d=d+0.2) {
	for (var e=0.6;e<=0.6;e=e+0.2) {
	
	var src = new IloOplModelSource( "project.template.mod" );
	var def = new IloOplModelDefinition( src );
	var cplex = new IloCplex();
	var model = new IloOplModel( def , cplex );
	var data = new IloOplDataSource( "generated_"+c+"_"+d+"_"+e+"_"+s+"_0.dat" );
	
	model . addDataSource( data );
	model . generate();
	
	var before = cplex.getCplexTime();
	
	
	cplex.epgap = 0.01 ;
	
	if (cplex.solve()) {
	  	//writeln( "------ Results for "+"la=0."+c+" dG=0."+d+" dH=0."+e+" ------");
		//writeln( "solution (optimal) with objective " + cplex.getObjValue () );
		for (var w in model.W) {
			var fw = 0;
  			for (var v in model.V) {
  	    		if (model.a[w][v] == 1) fw = v;
    		}
    		//writeln("f(" + w + ") = " + fw);
		}
		// Error Checking
		for (var w1 in model.W) {
		  for (var w2 in model.W) {
			for (var v1 in model.V) {
			  for (var v2 in model.V) {
				if (model.a[w1][v1] == 1 && model.a[w2][v2] == 1 && model.H[w1][w2] == 0 && model.G[v1][v2] > 0) {
					 writeln("error");
				}
			  }  	         
			}
		  }
		}
		var after = cplex.getCplexTime();
		//writeln("Running time ~= ", after-before);
		//writeln("Derteministic time ~= ", cplex.getDetTime());
		//writeln(model.n + model.m + c + d + e + cplex.getObjValue(int) + after-before + cplex.getDetTime());
		writeln(model.n + "," + model.m + "," + c + "," + d + "," + e + "," + cplex.getObjValue() + "," + (after-before) + "," + cplex.getDetTime())
	}				
	else {
		writeln ( "Not solution found" );
	}
	model.end ();
	data.end ();
	def.end ();
	cplex.end ();
	src.end ();
}}}
};