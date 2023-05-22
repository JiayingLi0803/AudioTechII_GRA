let data = [1, 5, 2, 3, 4];

let svg = d3.select("#svg1"),
  margin = { top: 20, right: 20, bottom: 30, left: 40 },
  width = +svg.attr("width") - margin.left - margin.right,
  height = +svg.attr("height") - margin.top - margin.bottom,
  g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scale.linear()
    .rangeRound([0, width])
    .domain([0, data.length]);
var y = d3.scale.linear()
    .rangeRound([height, 0])
    .domain([0, d3.max(data)]);

var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom");
var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left");


g.selectAll("line")
  .data(data)
  .enter().append("line")
  .attr("x1", (d, i) => x(i))
  .attr("y1", y(0))
  .attr("x2", (d, i) => x(i))
  .attr("y2", d => y(d))
  .style("stroke", "black");

g.selectAll("circle")
  .data(data)
  .enter().append("circle")
  .attr("cx", (d, i) => x(i))
  .attr("cy", d => y(d))
  .attr("r", 3)
  .style("fill", "black");


g.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);

//添加y轴
g.append("g")
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
    .domain([0, 5]);
var y2 = d3.scale.linear()
    .rangeRound([height2, 0])
    .domain([0, d3.max(data2)]);

var xAxis2 = d3.svg.axis()
  .scale(x2)
  .orient("bottom");
var yAxis2 = d3.svg.axis()
  .scale(y2)
  .orient("left");


g2.selectAll("line")
  .data(data2)
  .enter().append("line")
  .attr("x1", (d, i) => x2(i))
  .attr("y1", y2(0))
  .attr("x2", (d, i) => x2(i))
  .attr("y2", d => y2(d))
  .style("stroke", "black");

g2.selectAll("circle")
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

//添加y轴
g2.append("g")
  .attr("class", "axis")
  .call(yAxis2);