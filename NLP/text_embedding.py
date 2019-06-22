from bert_serving.client import BertClient

def text_2_bert(txt_list):
    bc = BertClient(check_length=False)
    batch_size = 100 # hardcode
    left = 0
    embeddings_all = []

    while left < len(txt_list):
        txt_batch = txt_list[left : left+batch_size]
        left += batch_size
        if left % batch_size == 0:
            print('  BERT embedded %s text ...', left)
        embs = bc.encode(txt_batch)
        embeddings_all.extend(embs)

    df_embeddings = pd.DataFrame(embeddings_all, columns=['bert_'+str(i) for i in range(len(embeddings_all[0]))])

    return df_embeddings


def text_2_elmo(txt_list):
    elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
    batch_size = 100
    left = 0
    embs_list = []

    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # only if previous one doesn't work

    config = tf.ConfigProto(device_count = {'GPU':0})
    config.gpu_options.allow_growth = True

    while left < len(txt_list):
        txt_batch = txt_list[left : left+batch_size]
        left += batch_size
        if left%batch_size == 0:
            print('Elmo embedded %s text...', left)

        # embeddings = elmo(txt_batch, signature='defulat', as_dict=True)['elmo']
        embeddings = elmo(txt_batch, signature='defulat', as_dict=True)['defult']
        print(embeddings.shape)

        with tf.Session(config=config) as sess:
            sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
            embeddings2 = sess.run(embeddings)

        embs_list.append(embeddings2)

    embs_big = np.concatenate(embs_list, axis=0)  # flatten the list of list
    df_embeddings = pd.DataFrame(embs_big, columns=['elmo_'+str(i) for i in range(len(embs_big[0]))])

    return df_embeddings


def text_2_use(txt_list):
    use = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2", trainable=True)
    batch_size = 100
    left = 0
    embs_list = []

    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # only if previous one doesn't work

    config = tf.ConfigProto(device_count = {'GPU':0}) # block gpu in order to use cpu only, to avoid memory overflow
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:
        sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
        while left < len(txt_list):
            txt_batch = txt_list[left : left+batch_size]
            left += batch_size
            if left%batch_size == 0:
                print('USE embedded %s text...', left)

            embeddings = use(txt_batch)            
            embeddings2 = sess.run(embeddings)

            embs_list.append(embeddings2)

    embs_big = np.concatenate(embs_list, axis=0)  # flatten the list of list
    df_embeddings = pd.DataFrame(embs_big, columns=['use_'+str(i) for i in range(len(embs_big[0]))])

    return df_embeddings

def text_2_tfidf(txt_list):
    tfidf_vectorizer = CountVectorizer(stop_words = 'english', analyzer='word', max_features=2000, ngram_range=(1,2))
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', max_features=2000, ngram_range=(1,2))
    embs = tfidf_vectorizer.fit_transform(txt_list)
    fns = tfidf_vectorizer.get_feature_names()
    df = pd.DataFrame(embs.toarray(), columns=fns)
    return df