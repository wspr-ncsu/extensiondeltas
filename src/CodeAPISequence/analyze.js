// LIBRARIES
const fs = require('fs'),
    path = require('path'),
    esprima = require('esprima'),
    crypto = require('crypto');


// ACTUAL CODE
// 2
// if (process.argv.length < 3) {
//     console.log('Usage: analyze.js file.js');
//     process.exit(1);
// }

// 3
// const outputPath = './allExtensionsAfterDiff/SequenceAPI';
// const filename = process.argv[2];

const moveFrom = 'allExtensionsAfterDiff/adds';
const moveTo = './allExtensionsAfterDiff/SequenceAPI';

loopThroughDir(moveFrom, moveTo);


// HERE START THE FUNCTIONS
function loopThroughDir(moveFrom, moveTo) {
    // Loop through all the files in the temp directory
    fs.readdir(moveFrom, function (err, files) {
        if (err) {
            console.error("Could not list the directory.", err);
            process.exit(1);
        }
        var counter = 0;
        files.forEach(function (file, index) {
        	counter += 1;
            // Make one pass and make the file complete
            var fromPath = path.join(moveFrom, file);
            var toPath = path.join(moveTo, file);

            fs.stat(fromPath, function (error, stat) {
                // if (error) {
                //     console.error("Error stating file.", error);
                //     return;
                // }

                // if (stat.isFile())
                //     console.log("'%s' is a file.", fromPath);
                // else if (stat.isDirectory())
                //     console.log("'%s' is a directory.", fromPath);


                // RENAME PART
                // fs.rename(fromPath, toPath, function (error) {
                //     if (error) {
                //         console.error("File moving error.", error);
                //     } 
                //     else {
                //         console.log("Moved file '%s' to '%s'.", fromPath, toPath);
                //     }
                // });

                try {
	                // console.log("From path = %s", fromPath);
                	console.log(fromPath);
	            	let apiSeq = analyzeCode(fromPath);
	                // console.log("This is the apiSeq %s\n", apiSeq);
	                fs.writeFile(toPath, apiSeq, function (error) {
	                    if(error) {
	                        console.error("Error on %s\n", toPath);
	                    }
	                    // else {
	                        // console.log("Successfully written file %s", toPath);
	                    // }
	                });
    			}
        		catch (e) {}

            });
        });
    	console.log(counter);
    });
};

function analyzeCode(filename) {
	console.log(filename);
    // const code = fs.readFileSync(filename, 'utf-8');    
    const code = fs.readFileSync(filename, 'ascii');    
    const tokens = esprima.tokenize(code.toString('utf8'));
    const tokenArray = Object.values(tokens);
    const filterId = tokenArray.filter(function(item){
        return item.type == 'Identifier' && item.value != '$';
    });
    const valuesOnly = filterId.map(t => t.value);
    // console.dir(valuesOnly, {'maxArrayLength': null} );
    return valuesOnly;
}