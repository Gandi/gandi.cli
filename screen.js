describe('landing page', function() {
    var client;
    before(function (done) {
        client = newClient();
        client
            .url(url || 'http://localhost:8042')
            .call(done);
    });
    after(function (done) {
        client.end(done);
    });
    it('should take screenshot', function (done) {
        client.screenstory('screenshot').call(done);
    });
});
