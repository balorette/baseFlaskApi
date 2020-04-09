import copy

class SyncMongo:
    """
    Instantiates Synchronous Mongo Client.

    For Synchronous IO to a Mongo Database, this class creates the client, then with built-in methods can handel
    standard operations.

    Attributes
    -----------
    uri : str
        The URI for the current DB

    db : str
        The name of the DB in side of Mongo

    Methods
    -----------

    write(collection, data)
        Writes a document to the Mongo DB

    read(collection, data)
        Reads information from the Mongo DB

    """
    from pymongo import MongoClient

    import bson

    def __init__(self, config):
        """
        Pass either a config file or a URI and DB in order to create the connection. Either use the config or the URI
        and DB values

        Parameters
        ---------
        config : Box
            A Box configured dictionary, should have two keys; uri and db
        """
        self._conf = config.db.mongo
        self.uri = self._conf.uri
        self.db = self._conf.db

        self._conn = self.MongoClient(self.uri)
        self._db = self._conn[self.db]


    def read(self, collection, docId=None, kvPair=None):
        """
        Read a document from a Mongo Collection.

        Parameters
        ----------
        collection : str
            The collection in which to read the document from
        docId :
            Either the string value of the document ID or the bson Object id type.
        kvPair : dict
            A key value pair for a query
        """

        if kvPair and type(kvPair) is dict:
            query = kvPair
        elif docId:
            if type(docId) is str:
                query= {'_id': self.bson.objectid.ObjectId(docId)}
            elif type(docId) is self.bson.objectid.ObjectId:
                query = {'_id': docId}
            else:
                print('Doc id only accepted as string or bson object id')
                return
        else:
            print('Please ensure your varialbes are set properly')
            return
        try:
            doc = self._db[collection].find_one(query)
            return doc
        except Exception as e:
            raise e

    def _check_exist(self, collection, data):
        """
        Internal function to check existence of data in the DB prior to write.
        """
        doc = self.read(collection, kvPair=data)
        if doc:
            return True

    def write(self, collection, data):
        """
        Write a document to a collection

        Parameters
        ----------

        collection : str
            The Collection to write the document to.
        data : dict
            The data to write as a python dictionary.

        """
        # @todo Validation check can be expanded.

        # Making a deep copy to ensure the passed object is not modified
        mongo_dict = copy.deepcopy(data)
        try:
            if self._check_exist(collection, mongo_dict):
                print('Document Already in Database, Did you mean to update?')
            else:
                doc_id = self._db[collection].insert_one(mongo_dict).inserted_id
                return {'_id': str(doc_id)}

        except Exception as e:
            print(e)
            raise Exception