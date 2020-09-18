public abstract class ShapeDecorator implements Shape{
    
    protected Shape decoratedShape;
    
    public ShapeDecorator(Shape deShape){
        this.decoratedShape = deShape;
    }

    public void draw(){
        this.decoratedShape.draw();
    }
}
