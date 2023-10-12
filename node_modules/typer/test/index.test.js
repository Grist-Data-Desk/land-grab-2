var typer  = require('../index.js'),
    assert = require('chai').assert;

describe('Cast', function () {
  describe('.cast()', function () {
    it('should properly cast to a boolean, false', function () {
      assert.strictEqual(typer.cast('false', 'bool'), false);
      assert.strictEqual(typer.cast('0', 'boolean'), false);
      assert.strictEqual(typer.cast(0, 'bool'), false);
      assert.strictEqual(typer.cast(false, 'bool'), false);
      assert.strictEqual(typer.cast(undefined, 'boolean'), false);
      assert.strictEqual(typer.cast(null, 'boolean'), false);
      assert.strictEqual(typer.cast('null', 'bool'), false);
      assert.strictEqual(typer.cast('undefined', 'boolean'), false);
    });

    it('should properly cast to a boolean, true', function () {
      assert.strictEqual(typer.cast(1, 'bool'), true);
      assert.strictEqual(typer.cast('true', 'boolean'), true);
      assert.strictEqual(typer.cast(true, 'boolean'), true);
      assert.strictEqual(typer.cast('foo', 'boolean'), true);
    });

    it('should properly cast to null for empty string', function () {
      assert.strictEqual(typer.cast(0, 'string'), null);
      assert.strictEqual(typer.cast(undefined, 'string'), null);
      assert.strictEqual(typer.cast('undefined', 'string'), null);
      assert.strictEqual(typer.cast(null, 'string'), null);
      assert.strictEqual(typer.cast('null', 'string'), null);
      assert.strictEqual(typer.cast(false, 'string'), null);
    });

    it('should properly cast to a string', function () {
      assert.strictEqual(typer.cast(23, 'string'), '23');
      assert.strictEqual(typer.cast('23', 'string'), '23');
      assert.strictEqual(typer.cast(23, 'string'), '23');
      assert.strictEqual(typer.cast('Foo bar bat baz bacon', 'string'), 'Foo bar bat baz bacon');
    });

    it('should properly cast to an integer', function () {
      assert.strictEqual(typer.cast(23, 'integer'), 23);
      assert.strictEqual(typer.cast('23', 'integer'), 23);
      assert.strictEqual(typer.cast(-23, 'integer'), -23);
      assert.strictEqual(typer.cast('-23', 'integer'), -23);
      assert.strictEqual(typer.cast('Foo bar bat baz bacon', 'integer'), 0);
    });

    it('should properly cast to a new Date', function () {
      var testDate = new Date('2016-02-22T18:00:00.000');

      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000', 'date'), testDate);
      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000Z', 'date'), testDate);
      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000', 'datetime'), testDate);
      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000Z', 'datetime'), testDate);
    });

    it('should properly cast to a float', function () {
      assert.strictEqual(typer.cast('23', 'float'), 23.00);
      assert.strictEqual(typer.cast(23, 'float'), 23.00);
      assert.strictEqual(typer.cast(-23, 'float'), -23.00);
      assert.strictEqual(typer.cast(23.12, 'float'), 23.12);
      assert.strictEqual(typer.cast(-23.12, 'float'), -23.12);
      assert.strictEqual(typer.cast('-23.12', 'float'), -23.12);
      assert.strictEqual(typer.cast('23.12', 'float'), 23.12);
      assert.deepEqual(typer.cast('foo', 'float'), NaN);
    });

    it('should smart-cast value', function () {
      assert.strictEqual(typer.cast(-23, 'smart'), -23);
      assert.strictEqual(typer.cast(23.12, 'smart'), 23.12);
      assert.strictEqual(typer.cast(-23.12, 'smart'), -23.12);
      assert.strictEqual(typer.cast('-23.12', 'smart'), -23.12);
      assert.strictEqual(typer.cast('false', 'smart'), false);
      assert.strictEqual(typer.cast('true', 'smart'), true);
      assert.strictEqual(typer.cast('null', 'smart'), null);
      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000', 'smart'), new Date('2016-02-22T18:00:00.000'));
      assert.deepEqual(typer.cast('2016-02-22T18:00:00.000Z', 'smart'), new Date('2016-02-22T18:00:00.000Z'));
    });
  });

  describe('.detect()', function () {
    it('should properly detect the type given (boolean)', function () {
      assert.strictEqual(typer.detect('false'), 'boolean');
      assert.strictEqual(typer.detect('true'), 'boolean');
    });

    it('should properly detect the type given (string)', function () {
      assert.strictEqual(typer.detect('null'), 'string');
      assert.strictEqual(typer.detect('foo'), 'string');
    });

    it('should properly detect the type given (integer using positive number)', function () {
      assert.strictEqual(typer.detect('12345'), 'integer');
      assert.strictEqual(typer.detect(12345), 'integer');
    });

    it('should properly detect the type given (integer using negative number)', function () {
      assert.strictEqual(typer.detect(-12345), 'integer');
      assert.strictEqual(typer.detect('-12345'), 'integer');
    });

    it('should properly detect the type given (float using positive number)', function () {
      assert.strictEqual(typer.detect('12345.12'), 'float');
      assert.strictEqual(typer.detect(12345.12), 'float');
    });

    it('should properly detect the type given (float using negative number)', function () {
      assert.strictEqual(typer.detect(-12345.12), 'float');
      assert.strictEqual(typer.detect('-12345.12'), 'float');
    });

    it('should properly fall back to string', function () {
      assert.strictEqual(typer.detect([]), 'string');
      assert.strictEqual(typer.detect({}), 'string');
    });

    it('should properly detect the type given (datetime)', function () {
      assert.strictEqual(typer.detect('2016-02-22T18:00:00.000Z'), 'datetime');
      assert.strictEqual(typer.detect('2016-02-22T18:00:00.000'), 'datetime');
    });
  });
});
