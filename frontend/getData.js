let fs = require('fs');

let getData = function(){
  let rawData = fs.readFileSync('../output.txt', 'utf8');
  let array = rawData.split("\n");

  let hash = {};

  array.forEach(function(line){
    let pair = line.split(": ");
    if(pair[0].length > 0){
      hash[pair[0]] = parseInt(pair[1]);
    }
  })
  return hash;
}

module.exports = getData;
