from IPython.display import display, Javascript

def autoupdate_cells(btn=None):
  js =  """
  function findCellIndicesByTag() {
    return Jupyter.notebook.get_cells().filter(function(cell) {
      // check that tags is defined and contains desired tag
      return cell.metadata && cell.metadata.autoupdate && (cell.metadata.autoupdate == true)
    }).map((cell) => Jupyter.notebook.find_cell_index(cell));
  }
  var autoupdate_cells = findCellIndicesByTag();
  console.log(autoupdate_cells);
  Jupyter.notebook.execute_cells(autoupdate_cells);
  """
  display(Javascript(js))