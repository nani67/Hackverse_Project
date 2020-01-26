/// id : "75f68777-5151-4b9e-9064-7331a8e74b84-f0f37969"
/// lang : "en"
/// sessionId : "12345"
/// timestamp : "2020-01-22T17:38:11.588Z"
/// result : {"source":"agent","resolvedQuery":"I need apples","action":"input.unknown","actionIncomplete":false,"score":1.0,"parameters":{},"contexts":[{"name":"shop","lifespan":4,"parameters":{}},{"name":"__system_counters__","lifespan":1,"parameters":{"no-input":0.0,"no-match":2.0}}],"metadata":{"intentId":"8e077430-a8ac-473b-9e63-acff3b144e64","intentName":"Default Fallback Intent","webhookUsed":"false","webhookForSlotFillingUsed":"false","isFallbackIntent":"true"},"fulfillment":{"speech":"Can you say that again?","messages":[{"lang":"en","type":0,"speech":"Can you say that again?"}]}}
/// status : {"code":200,"errorType":"success"}

class Schema {
  String id;
  String lang;
  String sessionId;
  String timestamp;
  ResultBean result;
  StatusBean status;

  static Schema fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    Schema schemaBean = Schema();
    schemaBean.id = map['id'];
    schemaBean.lang = map['lang'];
    schemaBean.sessionId = map['sessionId'];
    schemaBean.timestamp = map['timestamp'];
    schemaBean.result = ResultBean.fromMap(map['result']);
    schemaBean.status = StatusBean.fromMap(map['status']);
    return schemaBean;
  }

  Map toJson() => {
    "id": id,
    "lang": lang,
    "sessionId": sessionId,
    "timestamp": timestamp,
    "result": result,
    "status": status,
  };
}

/// code : 200
/// errorType : "success"

class StatusBean {
  int code;
  String errorType;

  static StatusBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    StatusBean statusBean = StatusBean();
    statusBean.code = map['code'];
    statusBean.errorType = map['errorType'];
    return statusBean;
  }

  Map toJson() => {
    "code": code,
    "errorType": errorType,
  };
}

/// source : "agent"
/// resolvedQuery : "I need apples"
/// action : "input.unknown"
/// actionIncomplete : false
/// score : 1.0
/// parameters : {}
/// contexts : [{"name":"shop","lifespan":4,"parameters":{}},{"name":"__system_counters__","lifespan":1,"parameters":{"no-input":0.0,"no-match":2.0}}]
/// metadata : {"intentId":"8e077430-a8ac-473b-9e63-acff3b144e64","intentName":"Default Fallback Intent","webhookUsed":"false","webhookForSlotFillingUsed":"false","isFallbackIntent":"true"}
/// fulfillment : {"speech":"Can you say that again?","messages":[{"lang":"en","type":0,"speech":"Can you say that again?"}]}

class ResultBean {
  String source;
  String resolvedQuery;
  String action;
  bool actionIncomplete;
  double score;
  ParametersBean parameters;
  List<ContextsBean> contexts;
  MetadataBean metadata;
  FulfillmentBean fulfillment;

  static ResultBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    ResultBean resultBean = ResultBean();
    resultBean.source = map['source'];
    resultBean.resolvedQuery = map['resolvedQuery'];
    resultBean.action = map['action'];
    resultBean.actionIncomplete = map['actionIncomplete'];
    resultBean.score = map['score'];
    resultBean.parameters = ParametersBean.fromMap(map['parameters']);
    resultBean.contexts = List()..addAll(
      (map['contexts'] as List ?? []).map((o) => ContextsBean.fromMap(o))
    );
    resultBean.metadata = MetadataBean.fromMap(map['metadata']);
    resultBean.fulfillment = FulfillmentBean.fromMap(map['fulfillment']);
    return resultBean;
  }

  Map toJson() => {
    "source": source,
    "resolvedQuery": resolvedQuery,
    "action": action,
    "actionIncomplete": actionIncomplete,
    "score": score,
    "parameters": parameters,
    "contexts": contexts,
    "metadata": metadata,
    "fulfillment": fulfillment,
  };
}

/// speech : "Can you say that again?"
/// messages : [{"lang":"en","type":0,"speech":"Can you say that again?"}]

class FulfillmentBean {
  String speech;
  List<MessagesBean> messages;

  static FulfillmentBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    FulfillmentBean fulfillmentBean = FulfillmentBean();
    fulfillmentBean.speech = map['speech'];
    fulfillmentBean.messages = List()..addAll(
      (map['messages'] as List ?? []).map((o) => MessagesBean.fromMap(o))
    );
    return fulfillmentBean;
  }

  Map toJson() => {
    "speech": speech,
    "messages": messages,
  };
}

/// lang : "en"
/// type : 0
/// speech : "Can you say that again?"

class MessagesBean {
  String lang;
  int type;
  String speech;

  static MessagesBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    MessagesBean messagesBean = MessagesBean();
    messagesBean.lang = map['lang'];
    messagesBean.type = map['type'];
    messagesBean.speech = map['speech'];
    return messagesBean;
  }

  Map toJson() => {
    "lang": lang,
    "type": type,
    "speech": speech,
  };
}

/// intentId : "8e077430-a8ac-473b-9e63-acff3b144e64"
/// intentName : "Default Fallback Intent"
/// webhookUsed : "false"
/// webhookForSlotFillingUsed : "false"
/// isFallbackIntent : "true"

class MetadataBean {
  String intentId;
  String intentName;
  String webhookUsed;
  String webhookForSlotFillingUsed;
  String isFallbackIntent;

  static MetadataBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    MetadataBean metadataBean = MetadataBean();
    metadataBean.intentId = map['intentId'];
    metadataBean.intentName = map['intentName'];
    metadataBean.webhookUsed = map['webhookUsed'];
    metadataBean.webhookForSlotFillingUsed = map['webhookForSlotFillingUsed'];
    metadataBean.isFallbackIntent = map['isFallbackIntent'];
    return metadataBean;
  }

  Map toJson() => {
    "intentId": intentId,
    "intentName": intentName,
    "webhookUsed": webhookUsed,
    "webhookForSlotFillingUsed": webhookForSlotFillingUsed,
    "isFallbackIntent": isFallbackIntent,
  };
}

/// name : "shop"
/// lifespan : 4
/// parameters : {}

class ContextsBean {
  String name;
  int lifespan;
  ParametersBean parameters;

  static ContextsBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    ContextsBean contextsBean = ContextsBean();
    contextsBean.name = map['name'];
    contextsBean.lifespan = map['lifespan'];
    contextsBean.parameters = ParametersBean.fromMap(map['parameters']);
    return contextsBean;
  }

  Map toJson() => {
    "name": name,
    "lifespan": lifespan,
    "parameters": parameters,
  };
}


class ParametersBean {

  static ParametersBean fromMap(Map<String, dynamic> map) {
    if (map == null) return null;
    ParametersBean parametersBean = ParametersBean();
    return parametersBean;
  }

  Map toJson() => {
  };
}
