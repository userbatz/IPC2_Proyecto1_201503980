// Grafo Campo agrícola 01
digraph {
	rankdir=LR
	e01 [label="Estación e01"]
	Ss1 [label="Sensor Suelo s01" shape=box]
	e01 -> Ss1 [label=700]
	Sc1 [label="Sensor Cultivo t01" shape=ellipse]
	e01 -> Sc1 [label=1500]
}
