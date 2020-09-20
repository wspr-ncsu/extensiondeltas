const fs = require('fs'),
    path = require('path'),
    esprima = require('esprima'),
    crypto = require('crypto');

 // PRODUCE API SEQUENCE
const myArgs = process.argv.slice(2);
fromPath = myArgs[0]
const file = myArgs[1]


// const moveFrom = 'allExtensionsAfterDiff/adds';
// const moveTo = './allExtensionsAfterDiff/SequenceAPI2';
const moveTo = '/media/nikos/fourTera1/homeA/javascriptCodeOut';


// const fromPath = path.join(moveFrom, file);
const toPath = path.join(moveTo, file);

// console.log(fromPath)
let apiSeq = analyzeCode(fromPath);
fs.writeFile(toPath, apiSeq, function (error) {
    if(error) {
        console.error("Error on %s\n", toPath);
    }
    // else {
        // console.log("Successfully written file %s", toPath);
    // }
});

function analyzeCode(filename) {
	// console.log(filename);
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

// const myArgs = process.argv.slice(2);
// fromPath = myArgs[0]
// file = myArgs[1]

// // CHANGE NEXT LINE
// // const moveTo = '/home/nikos/Documents/reviews_scripts/allExtensionsAfterDiff/wholeAST';
// const moveTo = 'media/nikos/fourTera1/homeA/vpcApi';

// const toPath = path.join(moveTo, file);
// console.log(toPath)

// try{
//     let apiSeq = produceASTHighLevel(fromPath);
//     // FIRST WAY
//     // fs.writeFile(toPath, JSON.stringify(apiSeq, null, 4), 'utf8', function (error) {

//     // SECOND WAY
//     fs.writeFile(toPath, JSON.stringify(apiSeq, null, 4), 'utf8', function (error) {
//         if(error) {
//             console.error("Error on %s\n", toPath);
//         }
//     });
// }
// catch(err){
//     console.log("Illegal Token = %s", err.message);
// }

// function produceASTHighLevel(filename) {
//     console.log(filename);
//     const code = fs.readFileSync(filename, 'utf-8');

//     // FiRST WAY ALL JSON FILE
//     // const ast = esprima.parse(code);

//     // SECOND WAY , COMMA SEPARATED AST NODES
//     const tokens = esprima.tokenize(code.toString('utf8'));
//     const tokenArray = Object.values(tokens);
//     const valuesOnly = tokenArray.map(t => t.type);

//     // RETURN RESULT
//     return valuesOnly
// }