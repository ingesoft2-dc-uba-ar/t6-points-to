package inge2.dataflow.targets;

public class Target1 {
    public void entryPoint() {
        Target1 a = new Target1();
        Target1 b = a; 
        Target1 c = b;
        Target1 d;
        d = a;
    }
}
