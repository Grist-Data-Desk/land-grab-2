# Typer
A small module that allows you to do simple type casting and detecting.

## Installation
`npm i --save typer`

## Usage
Usage is pretty simple. First, require typer and then use one of the documented methods.

### .detect(value)
Detect the type of `value`.

```javascript
var typer = require('typer');

console.log(typer.detect('12345.12')); // float
console.log(typer.detect('12345')); // integer
console.log(typer.detect('false')); // boolean
console.log(typer.detect('2016-02-22T18:00:00.000Z')); // datetime
```

You can find more examples in the tests.

### .cast(value, type='smart')
Cast `value` to `type`.

```javascript
var typer = require('typer');

console.log(typer.cast(23, 'string')); // '23'
console.log(typer.cast('23', 'integer')); // 23
console.log(typer.cast('23', 'float')); // 23.00
console.log(typer.cast('2016-02-22T18:00:00.000Z', 'date')); // Mon, 22 Feb 2016 18:00:00 GMT
