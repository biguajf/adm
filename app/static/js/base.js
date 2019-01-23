//função para CRSF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//Funçoes de navegação da pagina
/*
var mudou_pagina = true; 
function pagina(rota, titulo){
  $.ajax({url:rota})
  .done(function(data){ 
    var obj = JSON.stringify(data);
    var result = JSON.parse(obj);
    if(!$( '#id_li_content'+titulo.replace(/ /g,"")).length){
      var menu = '<li role="presentation" id="id_li_content'+titulo.replace(/ /g,"")+'" ><a href="#tab_content'+titulo.replace(/ /g,"")+'" role="tab" onclick=changeURL("'+rota+'","'+titulo+'") id="id_a_content'+titulo.replace(/ /g,"")+'" data-toggle="tab" aria-controls="profile" aria-expanded="false">'+ titulo +'<i class="i_close" onclick="fechaPagina('+"'"+titulo.replace(/ /g,"")+"'"+')">x</i></a></li>';
      var content = '<div role="tabpanel" class="tab-pane fade" id="tab_content'+titulo.replace(/ /g,"")+'" aria-labelledby="profile-tab">'+result.html+'</div>';
      $('#myTab1').append(menu);
      $('#myTabContent2').append(content);
    }
    $('#id_a_content'+titulo.replace(/ /g,"")).click();
    changeURL(rota,titulo);
  });
}

function changeURL(rota,titulo){
  mudou_pagina = true;
  window.location.href = '#0?r='+rota+'&t='+titulo.replace(/ /g,"");
}

function nextPage(id){
  var $li = $('#id_li_content'+id);  
  try {
    if($('#id_li_content'+id).hasClass('active')){
      if ($li.is(':first-child')) { // se for a primeira UL
          var $last = $li.find('li:last-child').attr("id").replace('id_li_content',"");
          $( '#id_li_content'+$last).addClass( "active");
          $( '#tab_content'+$last).addClass( "active in" );
      } else {
          var $last = $li.prev().attr("id").replace('id_li_content',"");
          $( '#id_li_content'+$last).addClass( "active");
          $( '#tab_content'+$last).addClass( "active in" );
      }
    }
  }catch(err) {
    return null;
  }
}

function fechaPagina(id){
  nextPage(id);
  $('#id_li_content'+id).remove();
  $('#tab_content'+id).remove();
}

// evento será chamado sempre q mudar a url
$.urlParam = function(name){
  var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
  if (results==null){
     return null;
  }
  else{
     return decodeURI(results[1]) || 0;
  }
}

$(window).bind('hashchange', function() {
  if(mudou_pagina){
    mudou_pagina = false;
  }else{
    var rota = $.urlParam('r');
    var titulo = $.urlParam('t');
    pagina(rota, titulo);    
  }
 });
*/
//Função para transformar o val dos inputs em maiusculo

$(document).on('blur', "input[type=text]", function () {
  $('input[type=text]').val (function () {
      return this.value.toUpperCase();
  });
});

//funções do arquivo csv
function downloadCSV(text, filename) {
    var pom = document.createElement('a');
    pom.setAttribute('href', "data:text/plain;base64," + btoa(text));
    pom.setAttribute('download', filename);
    pom.click();
}

function exportarTabelaCSV(id_tabela) {
    confirmar(  'Exportar arquivo CSV',
                '' +
                '<div class="roworm-group">' +
                '<label>Escolha o nome do arquivo .csv</label>' +
                '<input id="id_nome_arquivo_csv" type="text" placeholder="Nome do arquivo" class="name form-control" required />' +
                '</div>',
                'green',
                '',
                function () {
                    var nome_arquivo = this.$content.find('#id_nome_arquivo_csv').val();
                    if(!nome_arquivo){
                        alertar('Atenção','Digite um nome para o arquivo','red','fa fa-warning');
                        return false;
                    }
                    var csv = [];
                    var rows = document.querySelectorAll(id_tabela+" tr");

                    for (var i = 0; i < rows.length; i++) {
                        var row = [], cols = rows[i].querySelectorAll("td, th");
                        
                        for (var j = 0; j < cols.length; j++)
                            row.push(cols[j].innerText);
                        
                        csv.push(row.join(";"));
                    }
                    
                    downloadCSV(csv.join("\n"), nome_arquivo+".csv");
                },
                 function () {
                }
  );
}

function ImprimirTabela()
{
   var divToPrint=document.getElementById("datatable-buttons");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}


function formatarData(data,exibirHora=false){
  if (exibirHora==true){
    return moment(data).format('DD/MM/YYYY H:mm:ss')
  }else{
    return moment(data).format('DD/MM/YYYY')
  }
}

function formatarValor(valor,decimal=2){
  return valor.toLocaleString('pt-br',{ minimumFractionDigits: decimal , maximumFractionDigits: decimal })
}

 function clearClassBad(id){
    $("#"+id).parent(). removeClass("bad");
  }

function confirmar(titulo,mensagem,cor,icone,funcaoConfirmar,funcaoCancelar){
  $.confirm({
    title: titulo,
    content: mensagem,
    buttons: {
      confirmar: {
        text: 'Confirmar',
        btnClass: 'btn btn-round btn-success',
        action:funcaoConfirmar,
      },
      cancelar:{
        btnClass: 'btn btn-round btn-danger',
        text:'Cancelar',
        action: funcaoCancelar,
      },
    }
  });
}

function perguntar(titulo,mensagem,cor,icone,funcaoSim,funcaoNao){
  $.confirm({
    title: titulo,
    content: mensagem,
    type: cor,
    icon: icone,
    buttons: {
        sim:{ 
            text:'Sim',
            btnClass: 'btn btn-round btn-success',
            action: funcaoSim
        },
        nao:{
          text:'Não',
          btnClass: 'btn btn-round btn-danger',
          action: funcaoNao
        }
    }
  });
}

function alertar(titulo,mensagem,cor,icone){
  $.alert({
    title: titulo,
    content: mensagem,
    type: cor,
    icon: icone,
    autoClose: 'ok|3000',
    buttons:{
      ok:function () {
      }
    }
  });
}

function processar(titulo,mensagem,cor,funcao){
  $.dialog({
    title:titulo,
    content:mensagem,
    type:cor,
    icon:'fa fa-spinner fa-pulse fa-fw',
    buttons:{
    },
    onContentReady: funcao
  })
}

/*
function valorPresente(rValor,rJuros,iNParcelas)
{ 
  if (rJuros == 0){
    return (rValor/iNParcelas);
  }
  else {
    return rValor*((rJuros/100)/(1-(Math.pow(1/(1+(rJuros/100)),iNParcelas) )));           
  }
}
function carregarSelectConta(idCampo, filtroDefault = 0, idFinalizadora = 0){
  tempUrl = '/cadastros/finalizadoras/buscar/';
  $.ajax({
    data: {
      filtro : filtroDefault,
      id : idFinalizadora
    },
    type: 'GET',
    url:tempUrl
  }).success(function(data){
    var txt = '';
    for( i in data){
      txt = txt + '<option class="'+data[i].tipo_titulo+'" value="'+data[i]._id.$oid+'">'+data[i].descricao+'</option>';
    }
    $(idCampo).html(txt);
    $(idCampo).selectpicker("refresh");
  });
}
function carregarFinalizadoras(idCampo,valorDefault=[], filtroDefault = 0, idFinalizadora = 0){
  for (var i = idCampo.length - 1; i >= 0; i--) {
    $("#"+idCampo[i]).prev().prev().find('span.caret').addClass("fa fa-spinner fa-pulse fa-fw");
    $("#"+idCampo[i]).prev().prev().find('span.caret').removeClass('caret');
  }
  //
  $.ajax({
    data: {
      filtro : filtroDefault,
      id : idFinalizadora
    },
    type: 'GET',
    url:'/cadastros/finalizadoras/buscar/'
  }).success(function(data){
    var txt = '';
    for( i in data){
      txt = txt + '<option class="'+data[i].tipo_titulo+'" value="'+data[i]._id.$oid+'">'+data[i].descricao+'</option>';
    }
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).empty();
      $("#"+idCampo[i]).append(txt);
      //
      if (valorDefault[i]){
        $("#"+idCampo[i]).val(valorDefault[i]).change();
      }
      //
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
      //
      $("#"+idCampo[i]).selectpicker('refresh');
    };
  }).fail(function(data){
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
    }
  });
}

function carregarContas(idCampo,contaResultado= 0,valorDefault = []){  
  for (var i = idCampo.length - 1; i >= 0; i--) {
    $("#"+idCampo[i]).prev().prev().find('span.caret').addClass("fa fa-spinner fa-pulse fa-fw");
    $("#"+idCampo[i]).prev().prev().find('span.caret').removeClass('caret');
  }

  var tempUrl = ''
  tempUrl = '/contabil/contas/buscar/?resultado='+contaResultado;
  $.ajax({url:tempUrl})
  .success(function(data){
    var txt = '';        
    x = ''
    for (x in data.grupos){
      txt = txt+ '<optgroup label='+data.grupos[x].descricao+'>'
      var grupo = data.grupos[x].numero;
      var y = '';       
      for (y in data.contas){
        var conta_val = data.contas[y].conta;
        var conta_id = data.contas[y].id;
        if (conta_val.indexOf(grupo) != -1){              
          txt = txt+ '<option value="'+conta_id+'">'+data.contas[y].conta+' '+data.contas[y].descricao+'</option>'
        }
      }
      txt = txt + '</optgroup>'
    }
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).empty();
      $("#"+idCampo[i]).append('<option value="" disabled selected>---</option>');
      $("#"+idCampo[i]).append(txt);

      if (valorDefault[i]){
        $("#"+idCampo[i]).val(valorDefault[i]).change();       
      }
      //
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
      //
      $("#"+idCampo[i]).selectpicker('refresh');
    };
  }).fail(function(data){
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
    }
  });

}
*/
function carregarEntidade(idCampo,rota,grupo,limpar = true){
  for (var i = idCampo.length - 1; i >= 0; i--) {
    if (limpar){
      $("#"+idCampo[i]).empty();
      $("#"+idCampo[i]).append('<option value="" disabled selected>---</option>');
    }
    $("#"+idCampo[i]).prev().prev().find('span.caret').addClass("fa fa-spinner fa-pulse fa-fw");
    $("#"+idCampo[i]).prev().prev().find('span.caret').removeClass('caret');
  }
  $.ajax({url:'/buscar/'+rota})
  .success(function(data){
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).prev().find('span').removeClass('caret');
      $("#"+idCampo[i]).prev().find('span').addClass("fa fa-spinner fa-pulse fa-fw");
    }

    var txt = '';
    txt = txt+ '<optgroup label="'+grupo+'">'    
    for (i in data){          
      if (data[i].ativo==true){
        if(rota == 'produto'){
          txt = txt+ '<option value="'+data[i]._id['$oid']+'">'+data[i].nome+' - '+data[i].detalhes.marca+'</option>'
        }else{
          txt = txt+ '<option value="'+data[i]._id['$oid']+'">'+data[i].nome+'</option>'
        }
      }
      else{
        txt = txt+ '<option disabled value="'+data[i]._id['$oid']+'">'+data[i].nome+'</option>' 
      }
    }         
    txt = txt+ '</optgroup>'
    for (var i = idCampo.length - 1; i >= 0; i--) {   
      $("#"+idCampo[i]).append(txt);
      $("#"+idCampo[i]).selectpicker('refresh');
      //
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
    };
  }).fail(function(data){
    for (var i = idCampo.length - 1; i >= 0; i--) {
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').addClass('caret');
      $("#"+idCampo[i]).prev().prev().find('span.fa-spinner').removeClass("fa fa-spinner fa-pulse fa-fw");
    }
  });
}

function carregaMarca(idCampo){
  $("#"+idCampo).val('');
  $.ajax({
    url:'buscar/marca'
  }).success(function(data){
    var txt = '';
    for (i in data){          
        txt = txt+ '<option data-value="'+data[i]._id['$oid']+'">'+data[i].nome+'</option>';
    }
    $("#"+idCampo).html(txt);       
  });
}
/*
function gerarContas(){  
  $("#id_div_select_conta").html('<label class="control-label">Conta receita/despesa </label></br><select class="selectpicker form-control" data-live-search="true" id="id_conta_gerar_conta" placeholder="Teste" style="width: 100%"></select>');
  $("#id_conta_gerar_conta").selectpicker('refresh');
  
  $("#id_div_select_entidade").html('<div class="col-md-6 col-sm-12 col-xs-12 col-cx-12">'+
                                      '<label class="control-label">Devedor/Credor</label><br/>'+
                                      '<select class="selectpicker form-control" data-live-search="true" id="id_entidade_gerar_conta" style="width: 100%;"></select>'+
                                    '</div>'+
                                    '<div class="col-md-6 col-sm-12 col-xs-12 col-cx-12">'+
                                        '<label class="control-label">Previsão de conta</label><br/>'+
                                        '<select class="selectpicker form-control" data-live-search="true" id="id_finalizadora_previsao" style="width: 100%"></select>'+
                                    '</div>');

  $("#id_entidade_gerar_conta").selectpicker('refresh');
  $("#id_finalizadora_previsao").selectpicker('refresh');

  //
  $("#GeraContas").modal("show");
  $('#id_div_pago').show();
  $('#id_div_recorrencia').show();
  $('#id_separator').show();
  $('#id_div_valor_liquido').addClass('col-md-6 col-sm-6 col-xs-6');


  $('#id_historico_gerar_conta').prop('readonly', false);
  $('#id_valor_gerar_conta').prop('readonly', false);
  $('#id_input_data_competencia_gerar_conta').prop('readonly', false);
  $('#id_input_data_vencimento_gerar_conta').prop('readonly', false);
  
  mostrarGeraConta();

  //
  $("#id_entidade_gerar_conta").empty();
  $("#id_entidade_gerar_conta").append('<option value="" disabled selected>---</option>');
  //    
  carregarContas(['id_conta_gerar_conta'],1);
  carregarEntidade(['id_entidade_gerar_conta'],'cliente','Clientes',false); 
  carregarEntidade(['id_entidade_gerar_conta'],'fornecedor','Fornecedores',false);
  carregarEntidade(['id_entidade_gerar_conta'],'funcionario','Funcionários',false);
  carregarFinalizadoras(['id_finalizadora_gerar_conta','id_finalizadora_previsao']);
}

function transferirContas(){
  $('#TransfereConta').modal("show");
  carregarFinalizadoras(['id_transfere_conta_origem','id_transfere_conta_destino']);
}
*/
//Funções de endereço
function mostrarGradeEndereco(tipo_entidade){
  $("#"+tipo_entidade+"_id_edit_endereco").val('0');
  $("#"+tipo_entidade+"_grade_endereco").show();
  $("#"+tipo_entidade+"_btn_formulario_endereco").show();

  $("#"+tipo_entidade+"_btn_grade_endereco").hide();
  $("#"+tipo_entidade+"_formulario_endereco").hide();
}

function atualizarEndereco(entidade, tipo_entidade){
  var _url = '/buscar/'+tipo_entidade
  $.ajax({
    data: {
      id : $("#"+tipo_entidade+"_id").val(),
    },
    type: 'GET',
    url: _url
  }).success(function(data){
    endereco_html = '';
    for (j in data[0].endereco){
      var n = parseInt(j) + 1;
      endereco_html = endereco_html + '<tr>';
      endereco_html = endereco_html + '<th scope="row">'+n+'</th>';
      endereco_html = endereco_html + '<td>'+ data[0].endereco[j].tipo +'</td>';
      endereco_html = endereco_html + '<td>'+ data[0].endereco[j].tipo_logradouro+' '+data[0].endereco[j].logradouro+'</td>';
      endereco_html = endereco_html + '<td>'+ data[0].endereco[j].numero +'</td>';
      endereco_html = endereco_html + '<td>'+ data[0].endereco[j].bairro +'</td>';
      endereco_html = endereco_html + '<td>'+ data[0].endereco[j].cidade +'</td>';
      var parametro_edit_end = '"'+n+'",'+ JSON.stringify(data[0].endereco[j])+',"'+tipo_entidade+'"';
      endereco_html = endereco_html + "<td><i class='fa fa-pencil-square-o' aria-hidden='true' onclick='editarEndereco("+parametro_edit_end +")'></i>";    
      var parametro_excluir_end = '"'+ n +'","'+ data[0]._id['$oid']+'","'+tipo_entidade+'","'+entidade +'"';
      endereco_html = endereco_html + '<i class="fa fa-trash" aria-hidden="true" onclick=excluirEndereco('+ parametro_excluir_end +')></i>';
      endereco_html = endereco_html + '</td>';
      endereco_html = endereco_html + '</tr>';
    }
    $('#'+tipo_entidade+'_enderecos').html(endereco_html);
    mostrarGradeEndereco(tipo_entidade);
    switch(tipo_entidade) {
        case "cliente":
          buscarCliente();
          break;

        case "fornecedor":
          buscarFornecedor();;
          break;

        case "funcionario":
          buscarFuncionario();
          break;
      }
  }).fail(function(data){
    alertar('Atenção','Não foi possível buscar os endereços </br> Tente novamente mais tarde','red','fa fa-warning');
  });  
}

function adicionarEndereco(entidade, tipo_entidade){
  if($("#"+tipo_entidade+"_id").val() != '0'){
      var _url = '/adicionar/'+tipo_entidade
      $.ajax({
        data: {
          endereco : {
            id_endereco :$("#"+tipo_entidade+"_id_edit_endereco").val(),
            logradouro : $("#"+tipo_entidade+"_id_logradouro").val(),
            cidade : $("#"+tipo_entidade+"_id_cidade").val(),
            numero : $("#"+tipo_entidade+"_id_numero").val(),
            estado : $("#"+tipo_entidade+"_id_estado").val(),
            CEP : $("#"+tipo_entidade+"_id_CEP").val(),
            tipoLogradouro : $("#"+tipo_entidade+"_id_tipo_logradouro").val(),
            bairro : $("#"+tipo_entidade+"_id_bairro").val(),
            tipo : $("#"+tipo_entidade+"_id_tipo_endereco").val(),
            complemento : $("#"+tipo_entidade+"_id_complemento").val(),
            referencia : $("#"+tipo_entidade+"_id_referencia").val()
          },
          entidade : $("#"+tipo_entidade+"_id").val(),
        },
        type: 'POST',
        url: _url
      }).success(function(data){
        if(data.result == 1){
            mostrarFormularioEndereco(true,tipo_entidade);
            atualizarEndereco(entidade,tipo_entidade)
          }
        }).fail(function(data){
          alertar('Atenção','Edição não concluída </br> Tente novamente mais tarde','red','fa fa-warning');                          
      });
  } else {
      switch(tipo_entidade) {
        case "cliente":
          adicionarCliente(1);
          break;

        case "fornecedor":
          adicionarFornecedor(1);
          break;

        case "funcionario":
          adicionarFuncionario(1);
          break;
          
        case "medico":
          adicionarMedico(1);
          break;

        case "convenio":
          adicionarConvenio(1);
          break;    
      }
  } 
}

function excluirEntidade(id, tipo_entidade, entidade){
  confirmar('Atenção',
            'Deseja excluir esse '+entidade+'?',
            'red',
            'fa fa-warning',
            function () {
              $('#spinner_modal').modal('show');
              var self = this
              self.close();
              return $.ajax({
                data:{
                  id : id,
                },
                type: 'POST',
                url:'/excluir/entidade'               
              }).success(function(data){
                $('#spinner_modal').modal('hide');
                if(data.result == 0){
                  alertar('Atenção','Não foi possível excluir este registro </br> Tente novamente mais tarde','red','fa fa-warning');
                }
                $("#"+entidade+"_btn_ok").click();
              }).fail(function(data){
                alertar('Atenção','Não foi possível excluir este registro </br> Tente novamente mais tarde','red','fa fa-warning');
              });
            })
}

function excluirEndereco(id, cliente_id, tipo_entidade, entidade){
  confirmar('Atenção',
            'Deseja excluir este endereço?',
            'red',
            'fa fa-warning',
            function(){
              var self = this;
              self.close();
             return $.ajax({
                            data: {
                              deletar : {
                                idDel : id
                              },
                              entidade : cliente_id
                            },
                            type: 'POST',
                            url:'/excluir/endereco/'
                          }).success(function(data){
                            if(data.result == 1){
                              atualizarEndereco(entidade,tipo_entidade);
                            }
                          }).fail(function(data){
                              alertar('Atenção','Endereço não excluído </br> Tente novamente mais tarde','red','fa fa-warning');          
                          })
            }
          )
}

function editarEndereco(id, data, tipo_entidade){
  $('#'+tipo_entidade+'_id_edit_endereco').val(id);
  $('#'+tipo_entidade+'_id_tipo_endereco').val(data.tipo);
  $('#'+tipo_entidade+'_id_CEP').val(data.CEP);
  $('#'+tipo_entidade+'_id_tipo_logradouro').val(data.tipo_logradouro);
  $('#'+tipo_entidade+'_id_logradouro').val(data.logradouro);
  $('#'+tipo_entidade+'_id_numero').val(data.numero);
  $('#'+tipo_entidade+'_id_complemento').val(data.complemento);
  $('#'+tipo_entidade+'_id_bairro').val(data.bairro);
  $('#'+tipo_entidade+'_id_referencia').val(data.referencia);
  $('#'+tipo_entidade+'_id_cidade').val(data.cidade);
  $('#'+tipo_entidade+'_id_estado').val(data.estado);
  mostrarFormularioEndereco(false,tipo_entidade);
  $('.selectpicker').selectpicker("refresh");
}

function mostrarFormularioEndereco(limpar = true, tipo_entidade){
  if (limpar == true){
    $('#'+tipo_entidade+'_id_logradouro').val('');
    $('#'+tipo_entidade+'_id_cidade').val('');
    $('#'+tipo_entidade+'_id_numero').val('');
    $('#'+tipo_entidade+'_id_estado').val('');
    $('#'+tipo_entidade+'_id_CEP').val('');
    $('#'+tipo_entidade+'_id_tipo_logradouro').val('');
    $('#'+tipo_entidade+'_id_tipo_endereco').val('');
    $('#'+tipo_entidade+'_id_bairro').val('');
    $('#'+tipo_entidade+'_id_complemento').val('');
    $('#'+tipo_entidade+'_id_referencia').val('');
  }
  $('#'+tipo_entidade+'_grade_endereco').hide();
  $('#'+tipo_entidade+'_btn_formulario_endereco').hide();      

  $('#'+tipo_entidade+'_btn_grade_endereco').show();
  $('#'+tipo_entidade+'_formulario_endereco').show();
  //$('.selectpicker').selectpicker("refresh"); 
}


//Funções do contato
function mostrarGradeContato(tipo_entidade){
  $('#'+tipo_entidade+'_id_contato').val('0');
  $('#'+tipo_entidade+'_grade_contato').show();
  $('#'+tipo_entidade+'_btn_formulario_contato').show();

  $('#'+tipo_entidade+'_btn_grade_contato').hide();
  $('#'+tipo_entidade+'_formulario_contato').hide();
}

function atualizarContato(entidade, tipo_entidade){
  var _url = '/buscar/'+tipo_entidade
  if ($('#'+tipo_entidade+'_id').val() != 0){
    $.ajax({
      data: {
        id : $('#'+tipo_entidade+'_id').val(),
      },
      type: 'GET',
      url: _url }).success(function(value){
      contato_html = '';
      for (i in value[0].contato){
        var n = parseInt(i) + 1;
        contato_html = contato_html + '<tr>';
        contato_html = contato_html + '<th scope="row">'+n+'</th>';
        contato_html = contato_html + '<td>'+ value[0].contato[i].nome +'</td>';
        contato_html = contato_html + '<td>'+ value[0].contato[i].email +'</td>';
        contato_html = contato_html + '<td>'+ value[0].contato[i].telefone +'</td>';
        var parametro_edit_cont = "'"+ n +"','"+ value[0].contato[i].nome +"','"+ value[0].contato[i].email +"','"+ value[0].contato[i].telefone+"','"+tipo_entidade+"'";
        contato_html = contato_html + '<td><i class="fa fa-pencil-square-o" aria-hidden="true" onclick="editarContato('+ parametro_edit_cont +')"></i>';      
        var parametro_excluir_cont = "'"+ n +"','"+ value[0]._id["$oid"] +"','" +tipo_entidade+"','" +entidade+ "'";
        contato_html = contato_html + '<i class="fa fa-trash" aria-hidden="true" onclick="excluirContato('+ parametro_excluir_cont +')"></i>';
        contato_html = contato_html + '</td>';
        contato_html = contato_html + '</tr>';
      }
      $('#'+tipo_entidade+'_contatos').html(contato_html);
      mostrarGradeContato(tipo_entidade);
      switch(tipo_entidade) {
        case "cliente":
          buscarCliente();
          break;

        case "fornecedor":
          buscarFornecedor();;
          break;

        case "funcionario":
          buscarFuncionario();
          break;
      }
      }).fail(function(data){
          alertar('Atenção','Não foi possível buscar os contatos </br> Tente novamente mais tarde','red','fa fa-warning');                          
      });
  }
}
function adicionarContato(entidade, tipo_entidade){
  if($('#'+tipo_entidade+'_id').val() != '0'){
    var _url = '/adicionar/'+tipo_entidade
    $.ajax({
      data: {
        contato :{
          id_contato : $('#'+tipo_entidade+'_id_contato').val(),
          nome : $('#'+tipo_entidade+'_id_nome_contato').val(),
          email : $('#'+tipo_entidade+'_id_email_contato').val(),
          telefone : $('#'+tipo_entidade+'_id_telefone_contato').val()
        },
        entidade : $('#'+tipo_entidade+'_id').val(),
      },
      type: 'POST',
      url: _url
    }).success(function(data){
      if(data.result == 1){
        $('#'+tipo_entidade+'_id_nome_contato').val('');
        $('#'+tipo_entidade+'_id_email_contato').val('');
        $('#'+tipo_entidade+'_id_telefone_contato').val('');
        atualizarContato(entidade, tipo_entidade);
      }
      }).fail(function(data){
          alertar('Atenção','Edição não concluída </br> Tente novamente mais tarde','red','fa fa-warning');                          
      });
  }else {
    switch(tipo_entidade) {
      case "cliente":
        adicionarCliente(2);
        break;

      case "fornecedor":
        adicionarFornecedor(2);
        break;
      
      case "funcionario":
        adicionarFuncionario(2);
        break;

      case "medico":
        adicionarMedico(2);
        break;

      case "convenio":
        adicionarConvenio(2);
        break;
      }
    }
}

function excluirContato(id, id_cliente, tipo_entidade, entidade){
  confirmar('Atenção',
            'Deseja excluir este contato?',
            'red',
            'fa fa-warning',
            function(){
              var self = this;
              self.close();
             return $.ajax({
                        data: {
                          deletar : {
                            idDel : id
                          },
                          entidade : id_cliente
                        },
                        type: 'POST',
                        url:'/excluir/contato/'
                      }).success(function(data){
                        if(data.result == 1){
                          atualizarContato(entidade, tipo_entidade);
                        }
                      }).fail(function(data){
                          alertar('Atenção','Contato não excluído </br> Tente novamente mais tarde','red','fa fa-warning');                          
                        })
                    }
                )
}

function mostrarFormularioContato(limpar = true, tipo_entidade){
  if (limpar == true){
    $('#'+tipo_entidade+'_id_nome_contato').val('');
    $('#'+tipo_entidade+'_id_email_contato').val('');
    $('#'+tipo_entidade+'_id_telefone_contato').val('');
  }
  $('#'+tipo_entidade+'_grade_contato').hide();
  $('#'+tipo_entidade+'_btn_formulario_contato').hide();      

  $('#'+tipo_entidade+'_btn_grade_contato').show();
  $('#'+tipo_entidade+'_formulario_contato').show(); 
}

function editarContato(id, nome, email, telefone, tipo_entidade){
  $('#'+tipo_entidade+'_id_contato').val(id);
  $('#'+tipo_entidade+'_id_nome_contato').val(nome);
  $('#'+tipo_entidade+'_id_email_contato').val(email);
  $('#'+tipo_entidade+'_id_telefone_contato').val(telefone);
  mostrarFormularioContato(false,tipo_entidade);
}

// Função para deixar a tela em fullscreen
function fullScreen(){
  screenfull.request();
}

// Função para inserir val true ou false no ceckbox
function checkboxTrueFalse() { 
  $(".checkbox_true_false").on('change', function() {
    if ($(this).is(':checked')) {
      $(this).attr('value', true);
    } else {
      $(this).attr('value', false);
    } 
  });  
}

// Histórico
function historicoProduto(nome,marca,fornecedor = 0){
 $.ajax({
      data: {
        nome  : nome,
        marca : marca
      },
      type: 'GET',
      url:'/buscar/historicoProduto/'
    }).success(function(data){
      $('#id_modal_title').html('Histórico - '+ data[0].nome +' - ' + data[0].marca );
      var historico_html = '';
      var historico_body_html = '';
      $('#id_modal_lg').html(''); 
      for (i in data){
        for (j in data[i].fornecedor){
            if ($("#modal_"+data[i].fornecedor[j]._id).length){ 
              historico_body_html = historico_body_html + '<tr>';
              historico_body_html = historico_body_html + '<th scope="row">'+i+'</th>';
              historico_body_html = historico_body_html +'<td><p>'+ moment(data[i].data_cadastro['$date']).format('DD/MM/YYYY') +'</p></td>';
              //historico_body_html = historico_body_html +'<td><p>'+ data[i].fornecedor[j].nome +'</p></td>';
              historico_body_html = historico_body_html +'<td><p>R$'+ formatarValor(parseFloat(data[i].fornecedor[j].preco)) +'</p></td>';
              historico_body_html = historico_body_html + '</tr>';                   
            } else {
              if (fornecedor == data[i].fornecedor[j]._id || fornecedor == 0){
                historico_html = historico_html + '<h2>'+ data[i].fornecedor[j].nome +'</h2>';
                historico_html = historico_html + '<table class="table table-hover"><thead><tr name="parse_table"><th class="sorting" tabindex="0" aria-controls="datatable-buttons" style="width: 2%;" aria-sort="ascending">#</th><th class="sorting" tabindex="0" aria-controls="datatable-buttons" style="width: 18%;" aria-sort="ascending">Data</th><th class="sorting" tabindex="0" aria-controls="datatable-buttons" style="width: 80%;" aria-sort="ascending">Preço</th></tr></thead><tbody id="modal_'+data[i].fornecedor[j]._id+'"></tbody></table>';
                historico_body_html = historico_body_html + '<tr>';
                historico_body_html = historico_body_html + '<th scope="row">'+i+'</th>';
                historico_body_html = historico_body_html + '<td><p>'+ moment(data[i].data_cadastro['$date']).format('DD/MM/YYYY') +'</p></td>';
                historico_body_html = historico_body_html + '<td><p>R$'+ formatarValor(parseFloat(data[i].fornecedor[j].preco)) +'</p></td>';
                historico_body_html = historico_body_html + '</tr>';
                $('#id_modal_lg').append(historico_html);
              } 
            }
            $("#modal_"+data[i].fornecedor[j]._id).append(historico_body_html);
            historico_body_html = '';
            historico_html      = '';
        }
      };
      $('.bs-example-modal-lg').modal('show');
    });
}