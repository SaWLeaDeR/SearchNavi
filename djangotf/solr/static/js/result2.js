 
var pubs =
{
    "name": "Python",
    "children": [
        {
            "name": "Django","children": [
                {"name": "django-registration","children": [
                    {"name": "django-facebook "},
                    {"name": "django-profiles"}
                    
                ]},
                {"name": "django-authentication","children": [
                    {"name": "django-cms"}
                ]},
                {"name": "django-apps","children": [
                    {"name": "digital-ocean"},
                    {"name": "django-oscar"},
                    {"name": "django-sphinx "}
                ]},
                {"name": "django-models","children": [
                    {"name": "django-forms"},
                    {"name": "django-celery"}
                    
                ]},
                {"name": "django-admin","children": [
                    {"name": "django-channels"}
                ]}
            ]
        },
        {
            "name": "regex","children": [
                {"name": "replace"},
                {"name": "php"},
                {"name": "ruby"},
                {"name": "theory"},
                {"name": "javascript"},
                {"name": "perl"},
                {"name": "reluctant"},
                {"name": "beautifulsoup","children":[
                    {"name": "html"},
                    {"name": "innerhtml"},
                    {"name": "xml"},
                    {"name": "jython"},
                    {"name": "webcrawler"},
                    {"name": "mechanize"}
                ]}
            ]
        },
        {"name": "pip","children": [
        {
            "name": "python-2.7","children": [
                {"name": "ubuntu"},
                {"name": "scrapy"},
                {"name": "bash","children": [
                    {"name": "numpy"},
                    {"name": "matplotlib"},
                    {"name": "pypi"},
                    {"name": "curl","children":[
                        {"name": "kivy"},
                        {"name": "render"}
                    ]}
                ]},
            ]},
            {"name": "python-3.x","children": [
                    {"name": "linux"},
                    {"name": "scrapy"},
                    {"name": "basynchronous","children": [
                        {"name": "graph"},
                        {"name": "urllib"},
                        {"name": "typeerror "},
                        {"name": "combobox","children":[
                            {"name": "pyyaml "},
                            {"name": "aptana"},
                        ]}
                    ]
                    },
                
            ]},
        ]},
        {
            "name": "nlp","children": [
                {"name": "tagging"},
                {"name": "stemming"},
                {"name": "lemmatization"},
                {"name": "stop-words"},
                {"name": "part-of-speech"},
                {"name": "classification"},
                {"name": "probability"}
            ]
        },
        {
            "name": "solr","children": [
              {"name": "pysolr","children":[
                  {"name": "html"},
                  {"name": "xml"},
                  {"name": "tomcat"},
                  {"name": "json","children":[
                      {"name": "django"},
                      {"name": "highligt"},
                  ]}
              ]},
              
            ]
        }
    ]
};

var diameter = 800;

var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = diameter,
    height = diameter;
    
var i = 0,
    duration = 350,
    root;

var tree = d3.layout.tree()
    .size([360, diameter / 2 - 80])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 10) / a.depth; });

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select("#result").append("svg")
    .attr("width", width )
    .attr("height", height )
  .append("g")
    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

root = pubs;
root.x0 = height / 2;
root.y0 = 0;

//root.children.forEach(collapse); // start with all children collapsed
update(root);

d3.select(self.frameElement).style("height", "800px");

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root),
      links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 80; });

  // Update the nodes…
  var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      //.attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
      .on("click", click);

  nodeEnter.append("circle")
      .attr("r", 1e-6)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnter.append("text")
      .attr("x", 10)
      .attr("dy", ".35em")
      .attr("text-anchor", "start")
      //.attr("transform", function(d) { return d.x < 180 ? "translate(0)" : "rotate(180)translate(-" + (d.name.length * 8.5)  + ")"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  nodeUpdate.select("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeUpdate.select("text")
      .style("fill-opacity", 1)
      .attr("transform", function(d) { return d.x < 180 ? "translate(0)" : "rotate(180)translate(-" + (d.name.length + 50)  + ")"; });

  // TODO: appropriate transform
  var nodeExit = node.exit().transition()
      .duration(duration)
      //.attr("transform", function(d) { return "diagonal(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExit.select("circle")
      .attr("r", 1e-6);

  nodeExit.select("text")
      .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
      .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
  
  update(d);
}

// Collapse nodes
function collapse(d) {
  if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
}
