
function fixTotalFormsNumber()
{
	var inputNamePrefix = "exercises-",
		$parent = $( ".parent" );
	var count = $parent.find( "ul.exercise-form-data" ).length;
	$parent.find( "input[name=" + inputNamePrefix + "TOTAL_FORMS]" ).val( count );
}

/**
* Инициируем контролы
*/
function initiateControls()
{
	var $parent = $( ".parent" );
	$parent.find( ".controls .add" ).live( "click", function( Event ) { controlClicked( Event, "add" ) } );
	$parent.find( ".controls .delete" ).live( "click", function( Event ) { controlClicked( Event, "delete" ) } );
	$parent.find( ".controls .up" ).live( "click", function( Event ) { controlClicked( Event, "up" ) } );
	$parent.find( ".controls .down" ).live( "click", function( Event ) { controlClicked( Event, "down" ) } );
	updateControlsVisibility();
}

/**
* Скрывает "удалённые" заказы при перезагрузке страницы
*/
function hideDeletedExercises()
{
	var $hideExercisesInput = $( "input[name=hide_exercises]" );
	var hideByIndexes = $hideExercisesInput.val().split( "," );
	if ( hideByIndexes.length )
	{
		var $rows = $( ".exercise-form-data" );
		for ( var rowNum = 0, count = $rows.length; rowNum < count; rowNum ++ )
		{
			var $row = $( $rows[rowNum] );
			if ( $.inArray( rowNum + "", hideByIndexes ) > -1 ) {
				$row.hide();
			}
		}
	}
}

function updateControlsVisibility()
{
	var $rows = $( ".exercise-form-data:visible" );
	for ( var rowNum = 0, count = $rows.length; rowNum < count; rowNum ++ )
	{
		var $row = $( $rows[rowNum] );
		if ( rowNum == 0 ) {
			$row.find( ".up" ).hide();
		}
		else {
			$row.find( ".up" ).show();
		}
		if ( rowNum == ( count - 1 ) )
		{
			$row.find( ".down" ).hide();
			$row.find( ".add" ).show();
		}
		else
		{
			$row.find( ".down" ).show();
			$row.find( ".add" ).hide();
		}
		if ( count == 1 ) {
			$row.find( ".delete" ).hide();
		}
		else {
			$row.find( ".delete" ).show();
		}
	}
}

/**
* При клике на контрол
* @param Event
* @param string ControlType
*/
function controlClicked( Event, ControlType )
{
	if ( ControlType == "add" )
	{
		addNewExerciseInputs();
		updateControlsVisibility();
	}
	else
	{
		var $el = $( Event.target ),
			inputSelectors = [ "select[name$=name]", "input[name$=sets]" ],
			rowSelector = ".exercise-form-data";
		var $currentRow = $el.parents( rowSelector );
		if ( ControlType == "delete" )
		{
			deleteExercise( $currentRow, inputSelectors );
			updateControlsVisibility();
		}
		else
		{
			rowSelector += ":visible"
			var $changeToRow;
			if ( ControlType == "up" ) {
				$changeToRow = $currentRow.prevAll( rowSelector );
			}
			else {
				$changeToRow = $currentRow.nextAll( rowSelector )
			}
			if ( $changeToRow.length ) {
				$changeToRow = $changeToRow.eq( 0 );
			}
			changeExerciseInputValues( $currentRow, $changeToRow, inputSelectors );
		}
	}

/**
 * Добавляем поля ввода для ещё одного заказа
 */
	function addNewExerciseInputs()
	{
		var inputNamePrefix = "exercises-",
			$parent = $( ".parent" ),
		// в качестве шаболна используем последний ul для ввода упражнения
			$sourceExercise = $parent.find( "ul.exercise-form-data:last" );
	// если нашли ul и он правильный
		if ( $sourceExercise.length && $sourceExercise.find( "input[name^=" + inputNamePrefix + "]" ).length )
		{
		// для вычисления номера в шаблоне
			var re1 = new RegExp( inputNamePrefix + "(\\d*)-" );
		// для замены номеров
			var re2 = new RegExp( inputNamePrefix + "\\d*(-[^'\"]*)", "g" );
		// копируем html шаблона
			var newExerciseHtml = $sourceExercise.html();
		// получаем номер
			var sourceRowNum = parseInt( re1.exec( newExerciseHtml )[1] );
			var newRowNum = sourceRowNum + 1;
		// в html нового ul вписываем правильный номер
			newExerciseHtml = newExerciseHtml.replace( re2, inputNamePrefix + newRowNum + "$1" );
			$parent.append( "<ul class='exercise-form-data'>" + newExerciseHtml + "</ul>" );

		// увеличиваем количество форм для обработки на стороне сервера
			var $managerNums = $parent.find( "input[name=" + inputNamePrefix + "TOTAL_FORMS]" );
			$managerNums.val( parseInt( $managerNums.val() ) + 1 );
		}
	}

/**
 * "Удаляем" продукты
 */
	function deleteExercise( $Row, InputSelectors )
	{
		if ( $Row.length )
		{
		// с пустым параметром просто сбросит все значения
			exerciseData( $Row, InputSelectors, "set" );
			$Row.hide();
			// для скрывания этого упражнения при перезагрузке страницы
				var $hideExercisesInput = $( "input[name=hide_exercises]" );
				$hideExercisesInput.val( $hideExercisesInput.val() + $Row.index( "ul.exercise-form-data" ) + "," );

		}
	}

	/**
	 * Меняем два упражнения местами
	 * @param jquery $Row1
	 * @param jquery $Row2
	 * @param Array InputSelectors
	 */
	function changeExerciseInputValues( $Row1, $Row2, InputSelectors )
	{
		if ( $Row1.length && $Row2.length )
		{
			var row1Values = exerciseData( $Row1, InputSelectors, "get" ),
				row2Values = exerciseData( $Row2, InputSelectors, "get" );
			 exerciseData( $Row1, InputSelectors, "set", row2Values );
			 exerciseData( $Row2, InputSelectors, "set", row1Values );
		}
	}

/**
 * Геттер/сеттер всех инпутов упражнения (так сложно - чтобы сеттер всегда понимал формат геттера)
 * @param jquery $Row
 * @param Array InputSelectors
 * @param string Type - get/set
 * @param Array Values - для сеттера массив значений
 */
	function exerciseData( $Row, InputSelectors, Type, Values )
	{
		Type = Type == "set" ? "set" : "get";
		Values = Values ? Values : [];
	// Пробегаемся по всем нужным элементам ввода
	// если элемент элемент типа select, то получаем/заполняем выбранный option, для инпутов - то же самое с value
		for ( var i = 0, count = InputSelectors.length; i < count; i ++ )
		{
			var inputSelector = InputSelectors[i];
			var $input = $Row.find( inputSelector );
			if ( $input.is( "select" ) )
			{
				if ( Type == "get" ) {
					Values[i] = $input[0].selectedIndex;
				}
				else {
					$input[0].selectedIndex = i in Values ? Values[i] : 0;
				}
			}
			else
			{
				if ( Type == "get" ) {
					Values[i] = $input.val();
				}
				else {
					$input.val( i in Values ? Values[i] : "" );
				}
			}
		}
		return Values;
	}
}