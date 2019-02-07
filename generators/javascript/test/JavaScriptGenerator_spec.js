var assert = require('assert');
const GeneratedJs = require('../../../generated/js/catbuffer_generated_output');


describe('buffer_to_uint function', function () {
    it('buffer_to_uint converts a 1 byte unsigned integer', function(done) {
        var int8 = 76
        var array8 = new ArrayBuffer(1)
        var array8DataView = new DataView(array8)

        array8DataView.setUint8(0, int8)
        var int = GeneratedJs.buffer_to_uint(array8);
        assert.equal(int, int8);

        array8DataView.setUint8(0, 0)
        var int = GeneratedJs.buffer_to_uint(array8);
        assert.equal(int, 0);

        done();
    });

    it('converts a 2 byte unsigned integer', function(done) {
        var int16 = 76
        var array16 = new ArrayBuffer(2)
        var array16DataView = new DataView(array16)

        array16DataView.setUint16(0, int16)
        var int = GeneratedJs.buffer_to_uint(array16);
        assert.equal(int, int16);

        array16DataView.setUint16(0, 0)
        var int = GeneratedJs.buffer_to_uint(array16);
        assert.equal(int, 0);

        done();
    });

    it('converts a 4 byte unsigned integer', function(done) {
        var int32 = 76
        var array32 = new ArrayBuffer(4)
        var array32DataView = new DataView(array32)
        
        array32DataView.setUint32(0, int32)
        var int = GeneratedJs.buffer_to_uint(array32);
        assert.equal(int, int32);

        array32DataView.setUint32(0, 0)
        var int = GeneratedJs.buffer_to_uint(array32);
        assert.equal(int, 0);

        done();
    });
});

describe('concat_typedarrays function', function () {
    it('returns an empty array for two empty array inputs', function(done) {
        var array1 = new Uint8Array([])
        var array2 = new Uint8Array([])
        var result = GeneratedJs.concat_typedarrays(array1, array2)
        assert.deepEqual(Array.from(result), []);
        done();
    });

    it('returns original array if one of the params is empty', function(done) {
        var array1 = new Uint8Array([])
        var array2 = new Uint8Array([23, 54])

        var result = GeneratedJs.concat_typedarrays(array1, array2)
        assert.deepEqual(Array.from(result), Array.from(array2));
        var result2 = GeneratedJs.concat_typedarrays(array2, array1)
        assert.deepEqual(Array.from(result2), Array.from(array2));
        done();
    });

    it('returns the ordered concatenation of both params', function(done) {
        var array1 = new Uint8Array([23, 54])
        var array2 = new Uint8Array([34, 2, 77, 91, 12])

        var result = GeneratedJs.concat_typedarrays(array1, array2)
        assert.deepEqual(Array.from(result), Array.from(array1).concat(Array.from(array2)));
        var result2 = GeneratedJs.concat_typedarrays(array2, array1)
        assert.deepEqual(Array.from(result2), Array.from(array2).concat(Array.from(array1)));
        done();
    });
});

describe('concat_typedarrays function', function () {
    it('throws if data provided is larger than the requested output size', function(done) {
        assert.throws(GeneratedJs.fit_bytearray.bind(GeneratedJs, new Uint8Array([34, 2, 77, 91, 12]), 2), RangeError)
        done();
    });

    it('returns zero-initialized arrays for a null array input', function(done) {
        assert.deepEqual(GeneratedJs.fit_bytearray(null, 0), [])
        assert.deepEqual(GeneratedJs.fit_bytearray(null, 2), [0, 0])
        done();
    });

    it('returns the same array if the parameter size is the same as the parameter array length', function(done) {
        var array1 = new Uint8Array([])
        var array2 = new Uint8Array([34, 2, 77, 91, 12])

        assert.deepEqual(GeneratedJs.fit_bytearray(array1, array1.length), array1)
        assert.deepEqual(GeneratedJs.fit_bytearray(array2, array2.length), array2)
        done();
    });

    it('returns an array of the provided size initialized with trailing 0s if the input array was smaller', function(done) {
        var array1 = new Uint8Array([4])
        var array2 = new Uint8Array([34, 2, 77, 91, 12])

        assert.deepEqual(GeneratedJs.fit_bytearray(array1, 2), [0].concat(Array.from(array1)))
        assert.deepEqual(GeneratedJs.fit_bytearray(array2, 10), [0, 0, 0, 0, 0].concat(Array.from(array2)))
        done();
    });
});

describe('Uint8ArrayConsumableBuffer class', function () {
    it('constructs with buffer offset to 0, and stored array', function(done) {
        var array = new Uint8Array([34, 2, 77, 91, 12])
        var consumableBuffer = new GeneratedJs.Uint8ArrayConsumableBuffer(array)
        assert.equal(consumableBuffer.offset, 0)
        assert.deepEqual(consumableBuffer.binary, array)
        done();
    });

    it('get_bytes method throws if requesting more bytes than available', function(done) {
        var array1 = new Uint8Array([])
        var array2 = new Uint8Array([34, 2, 77, 91, 12])
        var consumableBuffer1 = new GeneratedJs.Uint8ArrayConsumableBuffer(array1)
        var consumableBuffer2 = new GeneratedJs.Uint8ArrayConsumableBuffer(array2)

        assert.throws(consumableBuffer1.get_bytes.bind(GeneratedJs.Uint8ArrayConsumableBuffer, array1.length + 1))
        assert.throws(consumableBuffer2.get_bytes.bind(GeneratedJs.Uint8ArrayConsumableBuffer, array2.length + 1))

        consumableBuffer2.offset = 5
        assert.throws(consumableBuffer2.get_bytes.bind(GeneratedJs.Uint8ArrayConsumableBuffer, 1))

        done();
    });

    it('get_bytes method returns requested bytes, and increases offset', function(done) {
        var array = [34, 2, 77, 91, 12]
        var consumableBuffer = new GeneratedJs.Uint8ArrayConsumableBuffer(new Uint8Array(array))

        var firstBatch = 2
        assert.deepEqual(consumableBuffer.get_bytes(firstBatch), array.slice(0, firstBatch))
        assert.equal(consumableBuffer.offset, firstBatch)

        var secondBatch = 3
        assert.deepEqual(consumableBuffer.get_bytes(secondBatch), array.slice(firstBatch, firstBatch + secondBatch))
        assert.equal(consumableBuffer.offset, firstBatch + secondBatch)

        done();
    });
});

describe('MosaicBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.MosaicBuffer()
        buffer.getMosaicid()
        buffer.setMosaicid(null)
        buffer.getAmount()
        buffer.setAmount(null)
        done();
    });

    it('loadFromBinary initializes from binary data', function(done) {
        var mosaicIdBuffer = Buffer.of(0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92)
        var mosaicAmountBuffer = Buffer.of(0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44)
        var consumableBuffer = new GeneratedJs.Uint8ArrayConsumableBuffer(Buffer.concat([
            mosaicIdBuffer,
            mosaicAmountBuffer,
        ]))
        var mosaicBuffer = GeneratedJs.MosaicBuffer.loadFromBinary(consumableBuffer)
        
        assert.deepEqual(mosaicBuffer.mosaicId, mosaicIdBuffer)
        assert.deepEqual(mosaicBuffer.amount, mosaicAmountBuffer)
        done();
    });

    it('serialize outputs a valid formatted buffer', function(done) {
        var mosaicBuffer = new GeneratedJs.MosaicBuffer()
        var mosaicIdBuffer = Buffer.of(0xF2, 0x26, 0x6C, 0x06, 0x40, 0x83, 0xB2, 0x92)
        var mosaicAmountBuffer = Buffer.of(0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44)
        mosaicBuffer.mosaicId = mosaicIdBuffer
        mosaicBuffer.amount = mosaicAmountBuffer

        var serializedData = mosaicBuffer.serialize()
        assert.deepEqual(serializedData, Buffer.concat([
            mosaicIdBuffer,
            mosaicAmountBuffer,
        ]))

        done();
    });
});

describe('SizePrefixedEntityBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.SizePrefixedEntityBuffer()
        buffer.getSize()
        buffer.setSize(null)
        done();
    });
});

describe('VerifiableEntityBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.VerifiableEntityBuffer()
        buffer.getSignature()
        buffer.setSignature(null)
        done();
    });
});

describe('EntityBodyBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.EntityBodyBuffer()
        buffer.getSigner()
        buffer.setSigner(null)
        buffer.getVersion()
        buffer.setVersion(null)
        buffer.getType()
        buffer.setType(null)
        done();
    });
});

describe('TransactionBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.TransactionBuffer()
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSignature()
        buffer.setSignature(null)
        buffer.getSigner()
        buffer.setSigner(null)
        buffer.getVersion()
        buffer.setVersion(null)
        buffer.getType()
        buffer.setType(null)
        buffer.getFee()
        buffer.setFee(null)
        buffer.getDeadline()
        buffer.setDeadline(null)
        done();
    });
});

describe('EmbeddedTransactionBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.EmbeddedTransactionBuffer()
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSigner()
        buffer.setSigner(null)
        buffer.getVersion()
        buffer.setVersion(null)
        buffer.getType()
        buffer.setType(null)
        done();
    });
});

describe('TransferTransactionBodyBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.TransferTransactionBodyBuffer()
        buffer.getRecipient()
        buffer.setRecipient(null)
        buffer.getMessage()
        buffer.setMessage(null)
        buffer.getMosaics()
        buffer.setMosaics(null)
        done();
    });
});

describe('TransferTransactionBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.TransferTransactionBuffer()
        buffer.getVersion()
        buffer.setVersion(null)
        buffer.setEntitytype(null)
        buffer.getEntitytype()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSignature(null)
        buffer.getSignature()
        buffer.setSigner(null)
        buffer.getSigner()
        buffer.setVersion(null)
        buffer.getVersion()
        buffer.setType(null)
        buffer.getType()
        buffer.setFee(null)
        buffer.getFee()
        buffer.setDeadline(null)
        buffer.getDeadline()
        buffer.setRecipient(null)
        buffer.getRecipient()
        buffer.setMessage(null)
        buffer.getMessage()
        buffer.setMosaics(null)
        buffer.getMosaics()
        done();
    });
});

describe('EmbeddedTransferTransactionBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.EmbeddedTransferTransactionBuffer()
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSigner()
        buffer.setSigner(null)
        buffer.getVersion()
        buffer.setVersion(null)
        buffer.getType()
        buffer.setType(null)
        buffer.getRecipient()
        buffer.setRecipient(null)
        buffer.getMessage()
        buffer.setMessage(null)
        buffer.getMosaics()
        buffer.setMosaics(null)
        done();
    });
});

describe('SizePrefixedEntityBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.SizePrefixedEntityBuffer()
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        done();
    });
});

describe('SizePrefixedEntityBuffer generated class', function () {
    it('has required getters and setters', function(done) {
        var buffer = new GeneratedJs.SizePrefixedEntityBuffer()
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        buffer.getSize()
        buffer.setSize(null)
        done();
    });
});
