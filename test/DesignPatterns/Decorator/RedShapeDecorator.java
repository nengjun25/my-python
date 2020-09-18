public class RedDecorator extends ShapeDecorate{
    
    public RedShapeDecorator(Shape shapeDecorator){
        super(shapeDecorator);
    }

    @overide
    public void draw(){
        super.decoratedShape.draw();
        myDraw();
    }

    public void myDraw(){
        System.out.println("Draw red");
    }


}
