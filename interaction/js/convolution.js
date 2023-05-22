let data = [1, 5, 2, 3, 4];

let svg = d3.select("#svg1"),
    margin = { top: 20, right: 20, bottom: 30, left: 40 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scale.linear()
    .rangeRound([0, width])
    .domain([0, 9]);
var y = d3.scale.linear()
    .rangeRound([height, 0])
    .domain([0, d3.max(data)]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

let lines = g.selectAll("line")
    .data(data)
    .enter().append("line")
    .attr("x1", (d, i) => x(i))
    .attr("y1", y(0))
    .attr("x2", (d, i) => x(i))
    .attr("y2", d => y(d))
    .attr("stroke-width", 1.5)
    .style("stroke", "black");

let circles = g.selectAll("circle")
    .data(data)
    .enter().append("circle")
    .attr("cx", (d, i) => x(i))
    .attr("cy", d => y(d))
    .attr("r", 3)
    .style("fill", "black");


g.append("svg:g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

//添加y轴
g.append("svg:g")
    .attr("class", "axis")
    .call(yAxis);


// graph 2

let data2 = [2, 4, 3, 6];

let svg2 = d3.select("#svg2"),
    margin2 = { top: 20, right: 20, bottom: 30, left: 40 },
    width2 = +svg.attr("width") - margin2.left - margin2.right,
    height2 = +svg.attr("height") - margin2.top - margin2.bottom,
    g2 = svg2.append("g").attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

var x2 = d3.scale.linear()
    .rangeRound([0, width2])
    .domain([0, 9]);
var y2 = d3.scale.linear()
    .rangeRound([height2, 0])
    .domain([0, d3.max(data2)]);

var xAxis2 = d3.svg.axis()
    .scale(x2)
    .orient("bottom");
var yAxis2 = d3.svg.axis()
    .scale(y2)
    .orient("left");


let lines2 = g2.selectAll("line")
    .data(data2)
    .enter().append("line")
    .attr("x1", (d, i) => x2(i))
    .attr("y1", y2(0))
    .attr("x2", (d, i) => x2(i))
    .attr("y2", d => y2(d))
    .attr("stroke-width", 1.5)
    .style("stroke", "black");

let circles2 = g2.selectAll("circle")
    .data(data2)
    .enter().append("circle")
    .attr("cx", (d, i) => x2(i))
    .attr("cy", d => y2(d))
    .attr("r", 3)
    .style("fill", "black");

g2.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height2 + ")")
    .call(xAxis2);

g2.append("g")
    .attr("class", "axis")
    .call(yAxis2);


// graph 3

// update graph width3, height3

function updateGraph() {
    let data3 = [2, 14, 27, 35, 56, 37, 30, 24];
    let svg3 = d3.select("#svg3"),
        margin3 = { top: 20, right: 20, bottom: 30, left: 40 },
        width3 = +svg.attr("width") - margin3.left - margin3.right,
        height3 = +svg.attr("height") - margin3.top - margin3.bottom,
        g3 = svg3.append("g").attr("transform", "translate(" + margin3.left + "," + margin3.top + ")");

    var x3 = d3.scale.linear()
        .rangeRound([0, width3])
        .domain([0, 9]);
    var y3 = d3.scale.linear()
        .rangeRound([height3, 0])
        .domain([0, d3.max(data3)]);

    var x3 = d3.scale.linear()
        .rangeRound([0, width2])
        .domain([0, 9]);
    var y3 = d3.scale.linear()
        .rangeRound([height3, 0])
        .domain([0, 60]);

    var xAxis3 = d3.svg.axis()
        .scale(x3)
        .orient("bottom");
    var yAxis3 = d3.svg.axis()
        .scale(y3)
        .orient("left");

    let lines3 = g3.selectAll("line")
        .data(data3)
        .enter().append("line")
        .attr("x1", (d, i) => x3(i))
        .attr("y1", y3(0))
        .attr("x2", (d, i) => x3(i))
        .attr("y2", d => y3(d))
        .attr("stroke-width", 1.5)
        .style("stroke", "black");

    let circles3 = g3.selectAll("circle")
        .data(data3)
        .enter().append("circle")
        .attr("cx", (d, i) => x3(i))
        .attr("cy", d => y3(d))
        .attr("r", 3)
        .style("fill", "black");
    g3.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height3 + ")")
        .call(xAxis3);
    
    g3.append("g")
        .attr("class", "axis")
        .call(yAxis3);
}



//svg 4
let svg4 = d3.select("#svg4"),
    margin4 = { top: 20, right: 20, bottom: 30, left: 40 },
    width4 = +svg.attr("width") - margin4.left - margin4.right,
    height4 = +svg.attr("height") - margin4.top - margin4.bottom,
    g4 = svg4.append("g").attr("transform", "translate(" + margin4.left + "," + margin2.top + ")");




// update text svg
var textStr = [];

function updateText(i, i2) {
    var d1 = data2[i];
    var d2 = data[i2];
    var out = d1 * d2;

    textStr.push(
        svg4.append('text')
            .attr("text-anchor", "end")
            .attr("x", 60 + i * 80 + i2 * 80)
            .attr("y", 10 + (i * 13))
            .text(d1 + "x" + d2 + "=" + out)
            .style("fill", "black")
            // .style("opacity", 0.0)
            .style("font-size", "12px")
    );

}

var sumStr = [];
function updateSum() {
    var val = [2, 14, 27, 35, 56, 37, 30, 24];
    for (l = 0; l < 8; l++) {

        sumStr.push(
            svg4.append('text')
                .attr("text-anchor", "end")
                .attr("x", 60 + l * 80)
                .attr("y", 72)
                .text("sum: " + val[l])
                .style("fill", "blue")
                // .style("opacity", 0.0)
                .style("font-size", "12px")

        )

    }

}


var playButton = d3.select('#play')
    .text("Play")
    .style("position", "relative")
    .style("top", 0)
    .style("left", 200)
    .style("height", 20)
    .on("click", handlePlay);



function restart(){
    d3.select("#svg4").selectAll("*").remove();
    d3.select("#svg3").selectAll("*").remove();

    textStr = [];
    sumStr = [];

}

function handlePlay() {
    playButton.attr("disabled", "disabled")
              .style("opacity", 0.5);
    restart();
    data2.forEach((d, i) => {
        setTimeout(() => {
            lines2
                .transition()
                .duration(500)
                .style("stroke", (_, j) => j === i ? "green" : "black");
            circles2
                .transition()
                .duration(500)
                .style("fill", (_, j) => j === i ? "green" : "black");

            data.forEach((d, i2) => {
                setTimeout(() => {
                    updateText(i, i2)
                    lines
                        .transition()
                        .duration(500)
                        .style("stroke", (_, j) => j === i2 ? "red" : "black");
                    circles
                        .transition()
                        .duration(500)
                        .style("fill", (_, j) => j === i2 ? "red" : "black");
                    if (i === 3 && i2 === 4) {
                        updateSum();
                        updateGraph();
                        playButton.attr("disabled", null)
                                  .style("opacity", 1);
                    }
                }, i2 * 1500);
            });
        }, i * 7500);
    });

}