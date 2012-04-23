/**
 * Created by PyCharm.
 * User: Roman
 * Date: 4/21/12
 * Time: 6:54 PM
 * To change this template use File | Settings | File Templates.
 */

/**
 * Updates the right side bar
 * @param state the current state of all nodes
 */
function updateRightSideBar() {
    // the current active tab
    var tab = $("#rightSidebar div.tab-content div.active").attr('id');

    if (tab === "rankings") {
        updateRankings(clusterState);
    }
}

function updateRankings(state) {
    // selected options
    var key = $("#rankings-data li.active").attr("name");
    var ascending = $("#rankings-order li.active").text() === "Ascending";

    // put state into array first, and sort
    var stateArray = [];
    for (var i in state) {
        if (state.hasOwnProperty(i) && i.search("machine") != -1) {
            stateArray.push(state[i]);
        }
    }
    stateArray.sort(function(a,b) {
        if (a[key] === b[key]) {
            return a.name < b.name ? -1 : 1;
        }
        else if (ascending) {
            return a[key] - b[key];
        }
        else {
            return b[key] - a[key];
        }
    });

    //only take first 10 sorted elements
    stateArray = stateArray.slice(0,10);

    //helper functions for D3
    var text = function(d) { return d.name + ": " + d[key].toFixed(2)};
    var height = function(i) { return i*25 + 20};
    var position = function(x) { return function(d,i) { return "translate(" + x + "," + height(i) + ")"; }};

    // update svg width + height, and bind data to the elements
    var rankings = d3.select("#rankings").select("svg")
        .attr("width", $('#rankings').width())
        .attr("height", 600)
        .selectAll("g")
        .data(stateArray, function(d) {return d.name;})
        .order();

    // add new nodes, which should slide in from the left
    var rankingsEnter = rankings.enter().append("g")
        .attr("transform", position(-100))
        .style("opacity", 1.0);

    rankingsEnter.append("text")
        .attr("class" , "sidebarText")
        .text(text);

    rankingsEnter.transition()
        .duration(500)
        .attr("transform", position(0));

    // update current nodes, which slide to their new position
    rankings.transition()
        .duration(500)
        .attr("transform", position(0))
        .style("opacity", 1.0)
        .select("text")
        .text(text);

    // exiting nodes slide to the bottom and fade off screen
    rankings.exit()
        .transition()
        .duration(500)
        .attr("transform", function(d,i) { return "translate(0," + height(10) + ")"; })
        .style("opacity", 0)
        .remove();
}