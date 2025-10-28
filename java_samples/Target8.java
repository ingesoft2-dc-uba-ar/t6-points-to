package inge2.dataflow.targets;

public class Target8 {
    private Target8 f1;

    public void entryPoint() {
        Target8 x = new Target8();
        Target8 y = new Target8();
        x.f = y;
        Target8 z = x.f;
    }
}