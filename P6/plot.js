
// css style of selected data point
var selectedStyle = {
    'r': 12,
    'fill': 'red',
    'stroke': 'black',
    'stroke-width': 2
};

function bySize_v1(data) {

    // create the chart
    var svg = dimple.newSvg("#itemPlot", "100%", "100%");
    window.myChart = new dimple.chart(svg, data);
    
    // setMargins is used instead of setBounds. The latter is not responsive
    myChart.setMargins(45, 75, 45, 35);
    
    // size as y-axis
    var y = myChart.addCategoryAxis("y", "size");
    y.addOrderRule("size");
    y.title = "Size (US)";
    
    // price as x-axis
    var x = myChart.addMeasureAxis("x", "price");
    x.title = "Price (US dollars)";
    
    // more information, lastly condition as our interactive filter
    var items = myChart.addSeries([
        "id",
        "shipping cost",
        "condition",
    ], dimple.plot.bubble, [x, y]);

    // average price of each available size as barplot layer
    var avg = myChart.addSeries([
        "average price for size",
    ], dimple.plot.bar, [x, y]);
    avg.aggregate = dimple.aggregateMethod.avg;
    // barplot to light grey
    myChart.assignColor("average price for size", "#222222", "#000000", 0.1);
    
    // add legend
    var myLegend = myChart.addLegend(0, 0, 100, 100, "left", items);
    
    myChart.draw();

    myChart.legends = [];

    // get a unique list of condition values to use when filtering
    var filterValues = dimple.getUniqueValues(data, "condition");
    
    // get all the rectangles from the legend
    myLegend.shapes.selectAll("rect")
        // Add a click event to each rectangle
        .on("click", function (e) {
            // this indicates whether the item is already visible or not
            var hide = false;
            var newFilters = [];
            // if the filters contain the clicked shape hide it
            filterValues.forEach(function (f) {
              if (f === e.aggField.slice(-1)[0]) {
                hide = true;
              } else {
                newFilters.push(f);
              }
            });
            // hide the shape or show it
            if (hide) {
              d3.select(this).style("opacity", 0.2);
            } else {
              newFilters.push(e.aggField.slice(-1)[0]);
              d3.select(this).style("opacity", 0.8);
            }
            // update the filters
            filterValues = newFilters;
            // filter the data
            myChart.data = dimple.filterData(data, "condition", filterValues);
            // passing a duration parameter makes the chart animate. Without
            // it there is no transition
            myChart.draw(800);
            // remark each scatterplot point with prepareDots function
            prepareDots(data);
        });
    // mark each scatterplot point with prepareDots function
    prepareDots(data);
}

// allow scatter points to become clickable and display the correct eBay item information
function prepareDots(data) {

    // if there is already a selected point, make sure it is styled properly
    if ( typeof selectedId !== 'undefined') {
        styleSelectedDot(selectedId);
    }

    // dots on click does ...
    d3.selectAll("circle").on("click", function (d) {

        $('#shoeInfo').hide();

        // change previously selected dot back to original styling  
        if ( typeof selectedId !== 'undefined' ) {
            $('#'+String(selectedId)).attr('style', originalStyle);
            $('#'+String(selectedId)).attr('r', 5);
        }
        // record newly selected dots id and original styling 
        window.originalStyle = $(this).attr('style');
        window.selectedId = $(this).attr('id');

        // change styling of newly selected dot
        if ( typeof selectedId !== 'undefined' ) {
            styleSelectedDot(selectedId);
        }

        // find right item from the data json array
        id = d.aggField[0]
        shoe = findId(id, data);
        //console.log(shoe);

        // display all relevant information
        $('#shoeStar').attr('src', 'https://s3.amazonaws.com/findmyshoes/base/ebay_stars/' + shoe.rating.toLowerCase() + '.gif')

        $('#shoeImage').attr('src', shoe.image);
        $('#shoePrice').text('$'+String(shoe.price));

        $('#shoeButton').attr('href', shoe.link);
        
        $('#shoeTitle').text(shoe.title);
        $('#shoeTitle').attr('href', shoe.link);
        
        $('#shoeSeller').text(shoe.seller);
        $('#shoeFeed').text("(" + shoe.feedbacks + ")");

        $('#shoeCond').text(shoe.condition);
        $('#shoeSize').text(shoe.size);
        $('#shoePayment').text(shoe.payment);
        $('#shoeShip').text(shoe['shipping cost']);
        $('#shoeHandle').text(shoe.handle + " days");
        $('#shoeOffer').text(shoe.offer);
        $('#shoeReturn').text(shoe.returns);

        $('#shoeInfo').show();
    
    });
}

// find item in array by id
function findId(id, a){
    for(var i = 0 ; i< a.length; i++){
        var obj = a[i];
        if (obj['id'] == id) {
            return obj;
        }
    }
}

// style using specified style
function styleSelectedDot(id) {
    $('#'+String(id)).css(selectedStyle);
}
