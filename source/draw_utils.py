from IPython.display import display, Javascript, display_javascript, HTML

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

import random
import string


def draw_nqueens(solutions):
  if solutions is None:
     display(HTML("The problem has no solutions"))
  solution = solutions[0]
  solution_js = '[' + ','.join(str(x) for x in solution) + ']'
  chessboard_id = 'chessboard_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

  display(HTML("""<div style="text-align:center;" id="%s"></div>""" % chessboard_id))
  if len(solutions)>1:
    display(HTML("Together with %d other solutions." % (len(solutions)-1)))

  draw_board_js = """ require['d3'];
    const queen = {
      name: "queen",
      w: "\u2655",
      b: "\u265B"
    };
    
    const boxSize = 50,
    boardDimension = %d,
    boardSize = boardDimension * boxSize,
    margin = 100;
    
    const solution = %s;
    
    // Get n queens solutions 
    // set <body>
    const div = d3.select("#%s");
    
    // create <svg>
    const svg = div.append("svg")
      .attr("width", boardSize + "px")
      .attr("height", boardSize + "px");
    
    // loop through 8 rows and 8 columns to draw the chess board
    for (let i = 0; i < boardDimension; i++) {
      for (let j = 0; j < boardDimension; j++) {
        // draw each chess field
        const box = svg.append("rect")
          .attr("x", i * boxSize)
          .attr("y", j * boxSize)
          .attr("width", boxSize + "px")
          .attr("height", boxSize + "px");
        if ((i + j) %% 2 === 0) {
          box.attr("fill", "beige");
        } else {
          box.attr("fill", "gray");
        }
    
        // draw chess pieces 
        const chess = svg.append("text")
          .style("font-size", '40')
          .attr("text-anchor", "middle")
          .attr("x", i * boxSize)
          .attr("y", j * boxSize)
          .attr("dx", boxSize / 2)
          .attr("dy", boxSize * 2 / 3);
        
        chess.attr("X", chess.attr("x"))
          .attr("Y", chess.attr("y"));
        // Draw pieces
        if (j === solution[i]) {
          chess.classed('queens', true)
            .text(queen.b);
        }
      }
    } """ % (len(solution), solution_js, chessboard_id)

  display(Javascript(draw_board_js))

def draw_us_map(map_colors):
  import matplotlib.pyplot as plt
  from mpl_toolkits.basemap import Basemap
  from matplotlib.patches import Polygon

  if map_colors is None:
    display(HTML("The problem has no solutions"))
    return

  map = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                projection='lcc', lat_1=33, lat_2=45, lon_0=-95)
  # load the shapefile, use the name 'states'
  map.readshapefile('assets/st99_d00', name='states', drawbounds=True)

  # Color states
  # collect the state names from the shapefile attributes so we can
  # look up the shape obect for a state by it's name
  state_names = []
  for shape_dict in map.states_info:
    state_names.append(shape_dict['NAME'])
  ax = plt.gca()  # get current axes instance
  # assign colors
  for state in map_colors:
    seg = map.states[state_names.index(state)]
    color = map_colors[state]
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

  plt.show()