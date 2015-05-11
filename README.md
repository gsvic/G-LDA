# G-LDA (Greek LDA)

<h1>Description</h1>
G-LDA is a project about Greek topic modeling/clustering. It applies Latent Dirichlet Allocation(LDA) extended with some modifications to work well on Greek text data. For this purpose, it uses <a href="https://github.com/skroutz/elasticsearch-skroutz-greekstemmer">elasticsearch-skroutz-greek-stemmer</a> for stop-word removal and stemming. The LDA algorithm is implemented with <a href="https://radimrehurek.com/gensim/">gensim</a>.

<h1>REST API</h1>
G-LDA also comes with a REST API in python <a href="http://flask.pocoo.org/">flask</a> that makes it's use very simple and flexible. It works with such plain GET/POST requests. For example, it returns the topic of a given document just by giving<br>
<code>CURL -X GET -G 'http://localhost:5000/classifier' -d text=YOUR_INPUT_DOC</code>

<h1>Deployment Instructions</h1>
Instructions for deployment will be added soon!

<h1>Contribution</h1>
G-LDA is a newly project and it may suffer from several issues. So feel free to share your ideas(and code) and contribute!
