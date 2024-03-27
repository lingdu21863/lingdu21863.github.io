/**@type {THMLCanvasElement} */

const canvas = document.getElementById('canvas1');
const ctx = canvas.getContext('2d');
CANVAS_WIDTH = canvas.width = window.innerWidth;
CANVAS_HEIGHT = canvas.height = window.innerHeight;
const numberOfEnemies = 10;
const enemiesArray = [];

class Enemy {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.width = Math.random() *20 + 30;
        this.height = this.width;
        this.speed = Math.random() * 3 + 1;
    }
    update() {
        
        if (this.x < -this.width || this.x > canvas.width -this.width) {
            this.speed = this.speed * -1;
        }
        //this.x -= this.speed * -1;
        this.x -= this.speed;

    }
    draw() {
        ctx.fillRect(this.x, this.y, this.width, this.height)
    }

};


for (let index = 0; index < numberOfEnemies; index++) {
    enemiesArray.push(new Enemy());
}


console.log(enemiesArray);

function animate() {
    //ctx.clearRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT);
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    enemiesArray.forEach(enemy => {
        enemy.update();
        enemy.draw();
    });
    requestAnimationFrame(animate);
}


animate();

