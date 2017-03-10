1. Python virtualenv
	Build new environment:
		virtualenv environment
	Start using environment:
		source environment/bin/activate
2. NodeJS nodeenv
	Build new environment:
		nodeenv nodejsEnvironment
	Start using environment:
		. nodejsEnvironment/bin/activate

3. PhantomJS
	nom install phantomjs // doesn’t work
	npm install phantomjs-prebuilt // work
	
4. CasperJS (install PhantomJS first)
	Inside the nodeJS virtual environment, using:
		npm install casperjs
		node_modules/casperjs/bin/casperjs selftest
