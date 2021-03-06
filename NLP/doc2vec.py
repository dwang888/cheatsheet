################ training
    print 'Traning ########################################'
    start_ts_train = datetime.now()
    model = Doc2Vec(min_count=10,
                    workers=size_worker,
                    iter= 30,
                    size=300,
                    dm=0, #defaul 1, distributed memory, similar to BOW in word2vec;
                    dm_concat=0,#default 0, faster; if 1, then very big input vector: concant all word vectors in doc
                    dbow_words = 1,#default 0. faster but doc vector only;
                    )  # use fixed learning rate
    '''In the PV-DBOW with skip-gram word-training ("dm=0, dbow_words=1") mode, 
    and the PV-DM modes without concatenation ("dm=1, dm_concat=0"), 
    the word and doc vectors are essentially trained into "the same space"
    '''
    logging.info('.. Build vocabulary')
    model.build_vocab(texts_all)
    logging.info('.. Train model')
    model.train(texts_all, 
                total_examples=len(texts_all), 
                epochs=model.iter,
                report_delay = 10,
                )
        
    model.init_sims(replace=True)
    print 'model trimed and saved'
    print 'model train time: ', datetime.now() - start_ts_train
    
    model_name = "D:\\projects\\fintech\\data\\doc2vec_sent_win300_dbow_word1_ltp.doc2vec"
    model.save(model_name, ignore=[])
    print len(model.wv.vocab), ' words learnt in model'
    print 'Word2Vec model training done, time: ', datetime.now()-start_ts
    
    #### testing
    model_name = "D:\\projects\\fintech\\data\\doc2vec_sent_win300_dbow_word1_ltp.doc2vec"
    model = Doc2Vec.load(model_name)
    print len(model.wv.vocab), ' words learnt in model'
    
    docvec2 = model.docvecs[0]
    print 'model.docvecs.doctag_syn0 shape', model.docvecs.doctag_syn0.shape
    docvecsyn2 = model.docvecs.doctag_syn0[0]
    
#     tokens_test = [u'两市', u'成交量', u'萎缩', u'总成交', u'金额']
    sent_test = "产能过剩".decode('utf-8')
    tokens_test = utils_nlp.text_2_ner_words(sent_test)
    doc0_inferred = model.infer_vector(tokens_test)
#     doc0_inferred = model.docvecs[0]    
    
    print ''.join(tokens_test)
    sims_to_infer = model.docvecs.most_similar([doc0_inferred], topn=200)
    for pair in sims_to_infer[:10]:
        id = pair[0]
        print pair
        print ''.join(id_2_text[id])
    
    print 'Doc2vec training done, time: ', datetime.now()-start_ts
    start_ts = datetime.now()
    
  
  
    testWords = ['习近平', '李克强', '钓鱼岛', '日本', '朝鲜', '台湾', '奥巴马', '科学', '发展观', '科学发展观', '港股',
                  "景顺医药","民企ETF","商品ETF","国企ETF", "军工","一带一路","保险","退欧","BREXIT","Brexit",
                  ]
    fund_short_names = get_funds_short_name_from_db()
    for w in testWords + fund_short_names:
        if w not in model.wv.vocab:
            continue
                            
        simWords = model.most_similar(w,topn=20)
        simWords = [item[0] for item in simWords]
        print '\n\n Most similar words to:\t', w
        print ' '.join(simWords[:20])

    conn.close()
    print 'model eval done, time: ', datetime.now()-start_ts
    print str(datetime.now())
    
    origin = model['未来']
    word_sims = [('word', word, score) for word, score in model.most_similar([origin],topn=20)]
    tag_sims = [('tag', tag, score) for tag, score in model.docvecs.most_similar([origin],topn=20)]
    results = sorted((tag_sims + word_sims),key=lambda tup: -tup[2])
    for rs in results[:40]:
        if rs[0] == 'word':
            print rs[2], rs[1] 
        if rs[0] == 'tag':
            print rs[2], ''.join(id_2_text[rs[1]])


###################################doc2vec model
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, Word2Vec
doc1 = TaggedDocument(words=text_tokens1, tags=['SENT_'+str(1)])
doc2 = TaggedDocument(words=text_tokens2, tags=['SENT_'+str(2)])
model = Doc2Vec(min_count=20, workers=14,)
model.build_vocab(texts_all)
model.train([doc1, doc2], total_examples=len(texts_all), epochs=50, report_delay = 600)
model.init_sims(replace=True)
model.save("path_to_model", ignore=[])
print len(model.wv.vocab), ' words learnt in model'

doc0_inferred = model.infer_vector([u'word1', u'word2', u'word3'])
sims_to_infer = model.docvecs.most_similar([doc0_inferred], topn=len(model.docvecs) )
for pair in sims_to_infer[:10]:
          id = pair[0]
          print pair
          print ''.join(id_2_text[id].words)



###################################################word2vec
from gensim.models import Word2Vec
from gensim.models import Phrases

text_segmented = [[word1, word2], [worda, wordb]]
bigram = Phrases(text_segmented)

model = Word2Vec(bigram[text_segmented], workers=8, size=100, min_count=10, window=5, sample=100000, sg=1)
pairs_sim = model.most_similar(target_w, topn=20)
word_vector = model.wv['computer']
