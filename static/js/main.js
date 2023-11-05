// variables
let userName = "test";
let state = "SUCCESS";

// functions
function Message(arg) {
  this.text = arg.text;
  this.message_side = arg.message_side;

  this.draw = (function (_this) {
    return function () {
      let $message;
      $message = $($(".message_template").clone().html());
      $message.addClass(_this.message_side).find(".text").html(_this.text);
      $(".messages").append($message);

      return setTimeout(function () {
        return $message.addClass("appeared");
      }, 0);
    };
  })(this);
  return this;
}

function getMessageText() {
  let $message_input;
  $message_input = $(".message_input");
  return $message_input.val();
}

function sendMessage(text, message_side) {
  let $messages, message;
  $(".message_input").val("");
  $messages = $(".messages");
  message = new Message({
    text: text,
    message_side: message_side,
  });
  message.draw();
  $messages.animate({ scrollTop: $messages.prop("scrollHeight") }, 300);
}

function greet() {
  setTimeout(function () {
    return sendMessage("안녕하세요.\n궁금하신 내용을 알려주세요.", "left");
  }, 1000);
  // setTimeout(function () {
  //     return sendMessage("Kochat 데모에 오신걸 환영합니다.", 'left');
  // }, 1000);
  // setTimeout(function () {
  //     return sendMessage("사용할 닉네임을 알려주세요.", 'left');
  // }, 2000);
}

function onClickAsEnter(e) {
  if (e.keyCode === 13) {
    onSendButtonClicked();
  }
}

function requestChat(messageText, url_pattern) {
  var formData = new FormData();
  formData.append('data', messageText);
  $.ajax({
    url: "http://127.0.0.1:8000/search/",
    type: "POST",
    // dataType: "json",
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      //   state = data["state"];
      console.log(data);
      return sendMessage(JSON.stringify(data["result"]), "left");
      // if (state === "SUCCESS") {
      //   return sendMessage(data["result"], "left");
      // } else if (state === "REQUIRE_LOCATION") {
      //   return sendMessage("어느 지역을 알려드릴까요?", "left");
      // } else {
      //   return sendMessage("죄송합니다. 무슨말인지 잘 모르겠어요.", "left");
      // }
    },

    error: function (request, status, error) {
      console.log(error);

      return sendMessage("죄송합니다. 서버 연결에 실패했습니다.", "left");
    },
  });
}

function onSendButtonClicked() {
  let messageText = getMessageText();
  sendMessage(messageText, "right");
  return requestChat(messageText, "request_chat");
  //   if (userName == null) {
  //     userName = setUserName(messageText);
  //   } else {
  if (messageText.includes("안녕")) {
    setTimeout(function () {
      return sendMessage("안녕하세요. 저는 Kochat 여행봇입니다.", "left");
    }, 1000);
  } else if (messageText.includes("고마워")) {
    setTimeout(function () {
      return sendMessage("천만에요. 더 물어보실 건 없나요?", "left");
    }, 1000);
  } else if (messageText.includes("없어")) {
    setTimeout(function () {
      return sendMessage("그렇군요. 알겠습니다!", "left");
    }, 1000);
  } else if (state.includes("REQUIRE")) {
    return requestChat(messageText, "fill_slot");
  } else {
    return requestChat(messageText, "request_chat");
  }
  //   }
}
