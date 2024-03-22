/**@type {THMLCanvasElement} */

const canvas = document.getElementById('canvas1');
const ctx = canvas.getContext('2d');
CANVAS_WIDTH = canvas.width = 2500;
CANVAS_HEIGHT = canvas.height = 2500;
const numberOfEnemies = 100;
const enemiesArray = [];

class Enemy{
    constructor(){
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.width = 50;
        this.height = 50;
        this.speed = Math.random() * 4 -2;
    }
    update(){
            this.x+= this.speed;
            this.y+= this.speed;
    }
    draw(){
        ctx.strokeRect(this.x,this.y,this.width,this.height)
    }

};


for (let index = 0; index < numberOfEnemies; index++) {
    enemiesArray.push(new Enemy());
}


console.log(enemiesArray);

function animate(){
    //ctx.clearRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT);
    ctx.clearRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT);
    enemiesArray.forEach(enemy => {
        enemy.update();
        enemy.draw();
    });
    requestAnimationFrame(animate);
}

animate();


